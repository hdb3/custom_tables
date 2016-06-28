
from ryu.ofproto.ofproto_v1_3_parser import OFPInstructionId,OFPActionId,OFPOxmId,OFPTableFeaturesStats,OFPTableFeaturePropInstructions,OFPTableFeaturePropNextTables, \
                                            OFPTableFeaturePropActions,OFPTableFeaturePropOxm
default_instruction_ids=[
  OFPInstructionId(len_=4,type_=1),
  OFPInstructionId(len_=4,type_=3),
  OFPInstructionId(len_=4,type_=4),
  OFPInstructionId(len_=4,type_=5),
  OFPInstructionId(len_=4,type_=6)
]

_default_action_ids=[
  OFPActionId(len_=4,type_=0),
  OFPActionId(len_=4,type_=17),
  OFPActionId(len_=4,type_=18),
  OFPActionId(len_=4,type_=22),
  OFPActionId(len_=4,type_=23),
  OFPActionId(len_=4,type_=25)
]


default_action_ids=[
  OFPActionId(len_=4,type_=0),
  OFPActionId(len_=4,type_=25)
]

oxm_eth_dst = OFPOxmId(hasmask=0,length=6,type_='eth_dst')
oxm_eth_src = OFPOxmId(hasmask=0,length=6,type_='eth_src')
oxm_vlan_vid = OFPOxmId(hasmask=0,length=2,type_='vlan_vid')
oxm_vlan_pcp = OFPOxmId(hasmask=0,length=1,type_='vlan_pcp')

table0 = OFPTableFeaturesStats(
  config=3,
  # length=376,
  max_entries=8192,
  metadata_match=0,
  metadata_write=0,
  name='Custom Single Table',
  table_id=0,
  properties=[
  ]
)

table1 = OFPTableFeaturesStats(
  config=3,
  # length=376,
  max_entries=8192,
  metadata_match=0,
  metadata_write=0,
  name='Custom Single Table',
  table_id=0,
  properties=[
    OFPTableFeaturePropInstructions(
      type_=0,
      instruction_ids=default_instruction_ids,
      length=24
    ),
    OFPTableFeaturePropInstructions(
      type_=1,
      instruction_ids=default_instruction_ids,
      length=24
    ),
#    OFPTableFeaturePropNextTables(
#      type_=2,
#      table_ids=[1, 2, 3],
#      length=7
#    ),
#    OFPTableFeaturePropNextTables(
#      type_=3,
#      table_ids=[1, 2, 3],
#      length=7
#    ),
    OFPTableFeaturePropActions(
      type_=4,
      action_ids=default_action_ids,
      # length=28
    ),
    OFPTableFeaturePropActions(
      type_=5,
      action_ids=default_action_ids,
#      length=28
    ),
    OFPTableFeaturePropActions(
      type_=6,
      action_ids=default_action_ids,
#      length=28
    ),
    OFPTableFeaturePropActions(
      type_=7,
      action_ids=default_action_ids,
#      length=28
    ),
    OFPTableFeaturePropOxm(
      type_=8,
      oxm_ids=[oxm_eth_src,oxm_vlan_vid],
      length=12
    ),
#    OFPTableFeaturePropOxm(
#      type_=10,
#      oxm_ids=[],
#      length=4
#    ),
    OFPTableFeaturePropOxm(
      type_=12,
      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
      length=20
#    ),
#    OFPTableFeaturePropOxm(
#      type_=13,
#      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
#      length=20
#    ),
#    OFPTableFeaturePropOxm(
#      type_=14,
#      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
#      length=20
#    ),
#    OFPTableFeaturePropOxm(
#      type_=15,
#      oxm_ids=[oxm_eth_dst,oxm_eth_src,oxm_vlan_vid,oxm_vlan_pcp],
#      length=20
    )
  ]
)
