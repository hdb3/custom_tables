
from ryu.ofproto.ofproto_v1_3_parser import OFPInstructionId,OFPActionId,OFPOxmId,OFPTableFeaturesStats,OFPTableFeaturePropInstructions,OFPTableFeaturePropNextTables, \
                                            OFPTableFeaturePropActions,OFPTableFeaturePropOxm

from maketable import makeTable

default_instruction_ids=[
  OFPInstructionId(len_=4,type_=1),
  OFPInstructionId(len_=4,type_=3),
  OFPInstructionId(len_=4,type_=4),
  OFPInstructionId(len_=4,type_=5),
  OFPInstructionId(len_=4,type_=6)
]

default_action_ids=[
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
####################
oxm_eth_dst_masked = OFPOxmId(hasmask=1,length=6,type_='eth_dst')
oxm_eth_src_masked = OFPOxmId(hasmask=1,length=6,type_='eth_src')
oxm_eth_type = OFPOxmId(hasmask=0,length=2,type_='eth_type')
oxm_ip_dscp = OFPOxmId(hasmask=0,length=1,type_='ip_dscp')
oxm_ip_proto = OFPOxmId(hasmask=0,length=1,type_='ip_proto')
oxm_ipv4_src_masked = OFPOxmId(hasmask=1,length=4,type_='ipv4_src')
oxm_ipv4_dst_masked = OFPOxmId(hasmask=1,length=4,type_='ipv4_dst')
oxm_tcp_src = OFPOxmId(hasmask=0,length=2,type_='tcp_src')
oxm_tcp_dst = OFPOxmId(hasmask=0,length=2,type_='tcp_dst')
oxm_udp_src = OFPOxmId(hasmask=0,length=2,type_='udp_src')
oxm_udp_dst = OFPOxmId(hasmask=0,length=2,type_='udp_dst')
oxm_ipv6_src_masked = OFPOxmId(hasmask=1,length=16,type_='ipv6_src')
oxm_ipv6_dst_masked = OFPOxmId(hasmask=1,length=16,type_='ipv6_dst')

tcam_match_oxm_ids=[oxm_eth_dst_masked,oxm_eth_src_masked,oxm_vlan_vid,oxm_vlan_pcp,oxm_eth_type,oxm_ip_dscp,oxm_ip_proto,oxm_ipv4_src_masked,oxm_ipv4_dst_masked, \
                    oxm_tcp_src,oxm_tcp_dst,oxm_udp_src,oxm_udp_dst,oxm_ipv6_src_masked,oxm_ipv6_dst_masked]

#####################

table0 = makeTable( max_entries=8192, name='Custom Single Table 0', table_id=0, next_tables=[], match_fields=[], set_fields=[])
_table0 = OFPTableFeaturesStats(
  config=3,
  max_entries=8192,
  metadata_match=0,
  metadata_write=0,
  name='Custom Single Table 0',
  table_id=0,
  properties=[
  ]
)

table1 = makeTable( max_entries=8192, name='Custom Single Table 0', table_id=0, next_tables=[], \
                    match_fields= [oxm_eth_src,oxm_vlan_vid], \
                    set_fields= [oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp])

_table1 = OFPTableFeaturesStats(
  config=3,
  max_entries=8192,
  metadata_match=0,
  metadata_write=0,
  name='Custom Single Table 1',
  table_id=0,
  properties=[
    OFPTableFeaturePropInstructions(
      type_=0,
      instruction_ids=default_instruction_ids,
    ),
    OFPTableFeaturePropInstructions(
      type_=1,
      instruction_ids=default_instruction_ids,
    ),
#    OFPTableFeaturePropNextTables(
#      type_=2,
#      table_ids=[1, 2, 3],
#    ),
#    OFPTableFeaturePropNextTables(
#      type_=3,
#      table_ids=[1, 2, 3],
#    ),
    OFPTableFeaturePropActions(
      type_=4,
      action_ids=default_action_ids,
    ),
    OFPTableFeaturePropActions(
      type_=5,
      action_ids=default_action_ids,
    ),
    OFPTableFeaturePropActions(
      type_=6,
      action_ids=default_action_ids,
    ),
    OFPTableFeaturePropActions(
      type_=7,
      action_ids=default_action_ids,
    ),
    OFPTableFeaturePropOxm(
      type_=8,
      oxm_ids=[oxm_eth_src,oxm_vlan_vid],
    ),
    OFPTableFeaturePropOxm(
      type_=10,
      oxm_ids=[],
    ),
    OFPTableFeaturePropOxm(
      type_=12,
      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
    ),
    OFPTableFeaturePropOxm(
      type_=13,
      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
    ),
    OFPTableFeaturePropOxm(
      type_=14,
      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
    ),
    OFPTableFeaturePropOxm(
      type_=15,
      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
    )
  ]
)
