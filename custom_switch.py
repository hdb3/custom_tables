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
from ryu.lib.packet import ethernet, arp, packet, ether_types
from ryu.ofproto.ofproto_v1_3_parser import OFPBarrierRequest as OFPB
from ryu.ofproto import ether
from pprint import pprint

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.request_generators = {}

    def request_generator(self,datapath):
        
        parser = datapath.ofproto_parser
        barrier_req = parser.OFPBarrierRequest(datapath)

        e = ethernet.ethernet(dst='ff:ff:ff:ff:ff:ff',
                              src='08:60:6e:7f:74:e7',
                              ethertype=ether.ETH_TYPE_ARP)
        a = arp.arp(hwtype=1, proto=0x0800, hlen=6, plen=4, opcode=2,
                    src_mac='08:60:6e:7f:74:e7', src_ip='192.0.2.1',
                    dst_mac='00:00:00:00:00:00', dst_ip='192.0.2.2')
        p = packet.Packet()
        p.add_protocol(e)
        p.add_protocol(a)
        p.serialize()
        msg1=p.data

        actions = [parser.OFPActionOutput(1, 0)]
        send_data_req = parser.OFPPacketOut(datapath, buffer_id=0xffffffff, in_port=datapath.ofproto.OFPP_CONTROLLER, actions=actions, data=p.data)

        print "send empty request"
        datapath.send_msg(barrier_req)
        yield
        print "send 1st datamsg"
        datapath.send_msg(send_data_req)
        datapath.send_msg(barrier_req)
        yield
        print "send 2nd datamsg"
        datapath.send_msg(send_data_req)
        datapath.send_msg(barrier_req)
        yield
        print "*** end of request sequence ***"
        yield

    @set_ev_cls(ofp_event.EventOFPBarrierReply, MAIN_DISPATCHER)
    def barrier_reply_handler(self, ev):
        datapath = ev.msg.datapath
        next(self.request_generators[datapath])

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        if (datapath.id == 1):
            print "configuring traffic datapath"
            match = parser.OFPMatch()
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
            self.add_flow(datapath, match, actions)
            self.request_generators[datapath] = self.request_generator(datapath)
            next(self.request_generators[datapath])
        elif (datapath.id == 2):
            print "configuring switch datapath"
            match = parser.OFPMatch(in_port=1)
            actions = [parser.OFPActionOutput(2)]
            self.add_flow(datapath, match, actions)

            match = parser.OFPMatch(in_port=2)
            actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath, match, actions)
        else:
            print "**NOT configuring unknown datapath: '%s'" % datapath.id



    @set_ev_cls(ofp_event.EventOFPTableFeaturesStatsReply, MAIN_DISPATCHER)
    def table_stats_reply_handler(self, ev):
        print "received table features response...."
        for table in ev.msg.body:
            print "table: name=%s id=%d size=%d" % (table.name, table.table_id,table.max_entries)

    def add_flow(self, datapath, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=0,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
