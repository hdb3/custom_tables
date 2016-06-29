
from ryu.ofproto.ofproto_v1_3_parser import OFPInstructionId,OFPActionId,OFPOxmId,OFPTableFeaturesStats,OFPTableFeaturePropInstructions,OFPTableFeaturePropNextTables, \
                                            OFPTableFeaturePropActions,OFPTableFeaturePropOxm
default_instruction_ids=[
  OFPInstructionId(len_=4,type_=1),
  OFPInstructionId(len_=4,type_=3),
  OFPInstructionId(len_=4,type_=4),
  OFPInstructionId(len_=4,type_=5),
  OFPInstructionId(len_=4,type_=6)
]

default_action_ids=[
  OFPActionId(len_=4,type_=0),
  OFPActionId(len_=4,type_=17),
  OFPActionId(len_=4,type_=18),
  OFPActionId(len_=4,type_=22),
  OFPActionId(len_=4,type_=23),
  OFPActionId(len_=4,type_=25)
]

valid_action_ids=[
  OFPActionId(len_=4,type_=0),
  # OFPActionId(len_=4,type_=17),
  # OFPActionId(len_=4,type_=18),
  OFPActionId(len_=4,type_=22),
  OFPActionId(len_=4,type_=23),
  OFPActionId(len_=4,type_=25)
]

oxm_in_port = OFPOxmId(hasmask=0,length=4,type_='in_port')
oxm_eth_dst = OFPOxmId(hasmask=0,length=6,type_='eth_dst')
oxm_eth_src = OFPOxmId(hasmask=0,length=6,type_='eth_src')
oxm_vlan_vid = OFPOxmId(hasmask=0,length=2,type_='vlan_vid')
oxm_vlan_pcp = OFPOxmId(hasmask=0,length=1,type_='vlan_pcp')

oxm_eth_type = OFPOxmId(hasmask=0,length=2,type_='eth_type')
oxm_ip_dscp = OFPOxmId(hasmask=0,length=1,type_='ip_dscp')
oxm_ip_proto = OFPOxmId(hasmask=0,length=1,type_='ip_proto')

oxm_ipv4_src = OFPOxmId(hasmask=0,length=4,type_='ipv4_src')
oxm_ipv4_dst = OFPOxmId(hasmask=0,length=4,type_='ipv4_dst')
oxm_ipv6_src = OFPOxmId(hasmask=0,length=16,type_='ipv6_src')
oxm_ipv6_dst = OFPOxmId(hasmask=0,length=16,type_='ipv6_dst')

oxm_tcp_src = OFPOxmId(hasmask=0,length=2,type_='tcp_src')
oxm_tcp_dst = OFPOxmId(hasmask=0,length=2,type_='tcp_dst')
oxm_udp_src = OFPOxmId(hasmask=0,length=2,type_='udp_src')
oxm_udp_dst = OFPOxmId(hasmask=0,length=2,type_='udp_dst')

oxm_eth_dst_masked = OFPOxmId(hasmask=1,length=6,type_='eth_dst')
oxm_eth_src_masked = OFPOxmId(hasmask=1,length=6,type_='eth_src')
oxm_ipv4_src_masked = OFPOxmId(hasmask=1,length=4,type_='ipv4_src')
oxm_ipv4_dst_masked = OFPOxmId(hasmask=1,length=4,type_='ipv4_dst')
oxm_ipv6_src_masked = OFPOxmId(hasmask=1,length=16,type_='ipv6_src')
oxm_ipv6_dst_masked = OFPOxmId(hasmask=1,length=16,type_='ipv6_dst')

match_fields= [oxm_eth_src,oxm_vlan_vid]
set_fields= [oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp]
L2_match = [oxm_eth_dst,oxm_eth_src,oxm_vlan_vid]

tcam_match=[
    oxm_in_port,
    oxm_eth_dst,
    oxm_eth_src,
    #oxm_eth_dst_masked,
    #oxm_eth_src_masked,
    #oxm_vlan_vid,
    #oxm_vlan_pcp,
    #oxm_eth_type,
    #oxm_ip_dscp,
    #oxm_ip_proto,
    oxm_ipv4_src,
    oxm_ipv4_dst,
    #oxm_ipv4_src_masked,
    #oxm_ipv4_dst_masked,
    #oxm_tcp_src,
    #oxm_tcp_dst,
    #oxm_udp_src,
    #oxm_udp_dst,
    #oxm_ipv6_src_masked,
    #oxm_ipv6_dst_masked
]

def makeTable(max_entries,name,table_id,next_tables,match_fields,set_fields,wild_fields=[],action_ids=valid_action_ids):
    return OFPTableFeaturesStats(

        config=3,
        max_entries=max_entries,
        metadata_match=0,
        metadata_write=0,
        name=name,
        table_id=table_id,
        properties=[
          OFPTableFeaturePropInstructions(
            type_=0,
            instruction_ids=default_instruction_ids,
          ),
          OFPTableFeaturePropInstructions(
            type_=1,
            instruction_ids=default_instruction_ids,
          )] + (
            [
             OFPTableFeaturePropNextTables(
               type_=2,
               table_ids=next_tables,
             ),
             OFPTableFeaturePropNextTables(
            type_=3,
            table_ids=next_tables,
             )
          ] if next_tables else [] ) + [
          OFPTableFeaturePropActions(
            type_=4,
            action_ids=action_ids,
          ),
          OFPTableFeaturePropActions(
            type_=5,
            action_ids=action_ids,
          ),
          OFPTableFeaturePropActions(
            type_=6,
            action_ids=action_ids,
          ),
          OFPTableFeaturePropActions(
            type_=7,
            action_ids=action_ids,
          ),
          OFPTableFeaturePropOxm(
            type_=8,
            oxm_ids=match_fields,
          ),
          OFPTableFeaturePropOxm(
            type_=10,
            oxm_ids=wild_fields,
          ),
          OFPTableFeaturePropOxm(
            type_=12,
            oxm_ids=set_fields,
          ),
          OFPTableFeaturePropOxm(
            type_=13,
            oxm_ids=set_fields,
          ),
          OFPTableFeaturePropOxm(
            type_=14,
            oxm_ids=set_fields,
          ),
          OFPTableFeaturePropOxm(
            type_=15,
            oxm_ids=set_fields,
          )
        ]
      )

# default pipelines

default_0_match = [oxm_eth_src,oxm_vlan_vid]
default_1_match = [oxm_eth_dst,oxm_vlan_vid]
default_2_match = [oxm_eth_type,oxm_vlan_vid,oxm_ip_proto,oxm_ipv4_src,oxm_ipv4_dst,oxm_tcp_src,oxm_tcp_dst,oxm_udp_src,oxm_udp_dst,oxm_ipv6_src,oxm_ipv6_dst]
default_3_match=[oxm_in_port,oxm_eth_dst_masked,oxm_eth_src_masked,oxm_eth_type,oxm_vlan_vid,oxm_vlan_pcp,oxm_ip_dscp,oxm_ip_proto,oxm_ipv4_src_masked,oxm_ipv4_dst_masked, \
                    oxm_tcp_src,oxm_tcp_dst,oxm_udp_src,oxm_udp_dst,oxm_ipv6_src_masked,oxm_ipv6_dst_masked]

default_3_wild=[oxm_in_port,oxm_eth_dst,oxm_eth_src,oxm_eth_type,oxm_vlan_vid,oxm_vlan_pcp,oxm_ip_dscp,oxm_ip_proto,oxm_ipv4_src_masked,oxm_ipv4_dst_masked, \
                    oxm_tcp_src,oxm_tcp_dst,oxm_udp_src,oxm_udp_dst,oxm_ipv6_src,oxm_ipv6_dst]

default_0_set = [oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp]
default_1_set = default_0_set
default_2_set = [oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp,oxm_ip_dscp,oxm_ipv4_src,oxm_ipv4_dst,oxm_tcp_src,oxm_tcp_dst,oxm_udp_src,oxm_udp_dst]
default_3_set = default_2_set

fudge_pipeline = [
    makeTable(8192,"Custom L2 Src",0,[1,2,3],default_0_match,default_0_set),
    makeTable(8192,"Custom L2 Dst",1,[2,3],default_1_match,default_1_set),
    makeTable(8192,"Custom L3 Table",2,[3],default_2_match,default_2_set),
    makeTable(8192,"Custom L3 Table 2",3,[],default_2_match,default_2_set)
]

default_pipeline = [
    makeTable(8192,"Custom L2 Src",0,[1,2,3],default_0_match,default_0_set),
    makeTable(8192,"Custom L2 Dst",1,[2,3],default_1_match,default_1_set),
    makeTable(8192,"Custom L3 Table",2,[3],default_2_match,default_2_set),
    makeTable(2016,"Custom TCAM Table",3,[],default_3_match,default_3_set,default_3_wild)
]

default_pipeline_table_0_1 = [
    makeTable(8192,"Custom L2 Src",0,[1],default_0_match,default_0_set),
    makeTable(8192,"Custom L2 Dst",1,[],default_1_match,default_1_set),
]

default_pipeline_table_0_2 = [
    makeTable(8192,"Custom L2 Src",0,[1,2],default_0_match,default_0_set),
    makeTable(8192,"Custom L2 Dst",1,[2],default_1_match,default_1_set),
    makeTable(8192,"Custom L3 Table",2,[],default_2_match,default_2_set),
]

default_pipeline_table_0 = [
    makeTable(8192,"Custom L2 Src",0,[],default_0_match,default_0_set),
]

default_pipeline_default_action_ids = [
    makeTable(8192,"Custom L2 Src",0,[1,2,3],default_0_match,default_0_set,[],default_action_ids),
    makeTable(8192,"Custom L2 Dst",1,[2,3],default_1_match,default_1_set,[],default_action_ids),
    makeTable(8192,"Custom L3 Table",2,[3],default_2_match,default_2_set,[],default_action_ids),
    makeTable(2016,"Custom TCAM Table",3,[],default_3_match,default_3_set,default_3_wild,default_action_ids)
]

default_pipeline_default_action_ids_table_0 = [
    makeTable(8192,"Custom L2 Src",0,[],default_0_match,default_0_set,[],default_action_ids),
]
