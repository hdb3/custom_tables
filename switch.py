# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
#from ryu.ofproto.ofproto_v1_3_parser import OFPBarrierRequest as OFPB
from maketable import *
from pprint import pprint

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.request_generators = {}
        self.reply_queues = {}
        self.barrier_req_xid  = {}

    def request_generator(self,datapath):

        def table_feature_parser(msgs):
            for msg in msgs:
                for table in msg.body:
                    print "table: name=%s id=%d size=%d" % (table.name, table.table_id,table.max_entries)
        
        def feature_set(pipeline):
            return self.parser.OFPTableFeaturesStatsRequest(datapath, 0, body=pipeline)

        datapath.name = ""
        if (datapath.id == 0x000b70106f911380):
          datapath.name = "dp11"
          # datapath.pipeline = simple_pipeline
          # datapath.pipeline = empty_pipeline
          datapath.pipeline = default_pipeline_table_0
          # datapath.pipeline = fudge_pipeline
          # datapath.pipeline = default_pipeline
        elif (datapath.id == 0x000c70106f911380):
          datapath.name = "dp12"
          datapath.pipeline = default_pipeline_table_0
        else:
          datapath.pipeline = empty_pipeline

        if (datapath.name):
          print "configuring datapath: '%s'" % datapath.name
        else:
          print "configuring datapath: '%016x'/'%016x'" % (datapath.id,datapath.xid)

        print "send table feature request"
        table_feature_parser((yield self.feature_req))

        for features in [default_pipeline,default_pipeline_table_0,fudge_pipeline,empty_pipeline,simple_pipeline]:
            print "send table feature reconfiguration"
            table_feature_parser((yield(feature_set(features))))


        # print "send table feature reconfiguration #1"
        # table_feature_parser((yield(feature_set(default_pipeline_table_0))))

        # print "send table feature reconfiguration #2"
        # table_feature_parser((yield(feature_set(default_pipeline))))

        print "send table feature request again"
        table_feature_parser((yield self.feature_req))

        print "*** end of request sequence ***"
        yield

    def run_generator(self, datapath):
        # this runs the generator to produce the next round of request messages, if any, and then sends them before exiting
        # on first invocation there are not yet any possible replies, however second and subsequent invocations will deliver queued response into the generator function
        rq = self.reply_queues[datapath]
        self.reply_queues[datapath] = []
        if (rq):
            msg=self.request_generators[datapath].send(rq)
        else:
            msg=self.request_generators[datapath].send(None)
        if (msg):
            datapath.send_msg(msg)
            self.barrier_req.xid = None
            datapath.set_xid(self.barrier_req)
            self.barrier_req_xid[datapath] = self.barrier_req.xid
            datapath.send_msg(self.barrier_req)

    @set_ev_cls(ofp_event.EventOFPBarrierReply, MAIN_DISPATCHER)
    def barrier_reply_handler(self, ev):
        # receipt of the barrier reply signals that all awaited actions are complete
        # if there have been any preceding error responses then they will already be on the reply queue, waiting to be delivered back to the generator
        # this function waits for the generator to run and produce the next round of request messages, if any
        datapath = ev.msg.datapath
        assert(self.barrier_req_xid[datapath] == ev.msg.xid)
        self.run_generator(datapath)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # this is the main datapath initialisation function
        # it's last job is to call the datapath driver generator function for the first time
        datapath = ev.msg.datapath
        self.parser = datapath.ofproto_parser
        self.reply_queues[datapath] = []
        self.barrier_req = self.parser.OFPBarrierRequest(datapath)
        self.feature_req = self.parser.OFPTableFeaturesStatsRequest(datapath, 0)
        self.request_generators[datapath] = self.request_generator(datapath)
        self.run_generator(datapath)


    @set_ev_cls(ofp_event.EventOFPTableFeaturesStatsReply, MAIN_DISPATCHER)
    def table_stats_reply_handler(self, ev):
        print "received table features response...."
        datapath = ev.msg.datapath
        self.reply_queues[datapath].append(ev.msg)
        print "appending response for datapath %s",datapath.name

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        else:
            msg = ev.msg
            datapath = msg.datapath
            in_port = msg.match['in_port']

            pkt = packet.Packet(msg.data)
            eth = pkt.get_protocols(ethernet.ethernet)[0]

            self.logger.info("packet in dp=%s src=%s dst=%s port=%s type=%s", datapath.id, eth.src, eth.dst, in_port, eth.ethertype)
