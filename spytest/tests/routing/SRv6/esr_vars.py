from spytest.dicts import SpyTestDict

data = SpyTestDict()

data.ecmp_dut1_portlist = ['Ethernet3', 'Ethernet4']
data.ecmp_dut2_portlist = ['Ethernet3', 'Ethernet4']
data.ecmp_member_Gbps = 58

data.ecmp_503_504_dut1_dut2_portlist = ['Ethernet12', 'Ethernet16', 'Ethernet28', 'Ethernet32', 'Ethernet44', 'Ethernet60']
data.ecmp_503_504_dut_tg_portlist = ['Ethernet109', 'Ethernet110']
data.ecmp_501_502_dut1_dut2_portlist = ['Ethernet92', 'Ethernet96', 'Ethernet108']
data.ecmp_501_502_dut_RJ_portlist = ['Ethernet8', 'Ethernet9', 'Ethernet10', 'Ethernet11']
data.ecmp_501_502_dut_tg_portlist = ['Ethernet111', 'Ethernet112']
data.dut_ecmp_scale_start_subintf = '201'
data.dut_ecmp_scale_subintf_num = 13
data.dut_isolate_group_num = 6
data.dut_bfd_port_list = ['Ethernet13']
data.dut1_vrf1_ip_addr = ["12.109.104.2", "12.110.104.2", "12.111.100.2", " 12.112.100.2"]
data.dut1_vrf1_ipv6_addr = ["fd40:12:109:104::2", "fd40:12:110:104::2", "fd40:12:111:100::2", "fd40:12:112:100::2"]
data.dut1_vrf1_id = ["503", "503", "501", "501"]
data.dut1_vrf2_ip_addr = ["12.109.106.2", "12.110.106.2", "12.111.102.2", "12.112.102.2"]
data.dut1_vrf2_ipv6_addr = ["fd40:12:109:106::2", "fd40:12:110:106::2", "fd40:12:111:102::2", "fd40:12:112:102::2"]
data.dut1_vrf2_id = ["504", "504", "502", "502"]
data.dut_traffic_vrf_name = {"501": "long-vrf-501", "502": "long-vrf-502",
                            "503": "long-vrf-503", "504": "long-vrf-504"}
data.dut_tg_bfd_vrf_name = {"TG1_1":"long-vrf-TG-bfd1", "TG1_2":"long-vrf-TG-bfd2",
                            "TG1_3":"long-vrf-TG-bfd3", "TG1_4":"long-vrf-TG-bfd4"}
data.dut1_dut2_bfd_vrf_name = ["long-vrf-dut-bfd1"]

data.dut2_vrf1_ip_addr = ["11.109.104.1", "11.110.104.1"]
data.dut2_vrf1_ipv6_addr = ["fd40:11:109:104::1", "fd40:11:110:104::1"]
data.dut2_vrf1_id = ["503", "503"]
data.dut2_vrf2_ip_addr = ["11.109.106.1", "11.110.106.1"]
data.dut2_vrf2_ipv6_addr = ["fd40:11:109:106::1", "fd40:11:110:106::1"]
data.dut2_vrf2_id = ["504", "504"]

data.dut3_vrf1_ip_addr = ["11.61.100.1", "11.62.100.1"]
data.dut3_vrf1_id = ["501", "501"]
data.dut3_vrf2_ip_addr = ["11.61.102.1", "11.62.102.1"]
data.dut3_vrf2_id = ["502", "502"]

data.dut1_bfdv4_start_ip_addr = ["109.1.0.1","110.2.0.1","111.3.0.1", "112.4.0.1"]
data.dut1_bfdv6_start_ip_addr = ["109:1::1","110:2::1","111:3::1", "112:4::1"]
data.dut2_bfdv4_start_ip_addr = ["109.1.0.1","110.2.0.1"]
data.dut2_bfdv6_start_ip_addr = ["109:1::1","110:2::1"]
data.tg1_bfdv4_start_ip_addr = ["109.1.0.2","110.2.0.2","111.3.0.2", "112.4.0.2"]
data.tg1_bfdv6_start_ip_addr = ["109:1::2","110:2::2","111:3::2", "112:4::2"]
data.tg2_bfdv4_start_ip_addr = ["109.1.0.2","110.2.0.2"]
data.tg2_bfdv6_start_ip_addr = ["109:1::2","110:2::2"]

data.tg1_vrf1_ip_addr = ["12.109.104.1", "12.110.104.1", "12.111.100.1", "12.112.100.1"]
data.tg1_vrf1_ipv6_addr = ["fd40:12:109:104::1", "fd40:12:110:104::1", "fd40:12:111:100::1", "fd40:12:112:100::1"]
data.tg1_vrf2_ip_addr = ["12.109.106.1", "12.110.106.1", "12.111.102.1", "12.112.102.1"]
data.tg1_vrf2_ipv6_addr = ["fd40:12:109:106::1", "fd40:12:110:106::1", "fd40:12:111:102::1", "fd40:12:112:102::1"]
data.tg1_vrf1_router_prefix_list = ["202.1.0.0", "202.1.0.0", "204.1.0.0", "204.1.0.0"]
data.tg1_vrf1_router_v6_prefix_list = ["3000:1::1", "3000:1::1", "3000:2::1", "3000:2::1"]
data.tg1_vrf2_router_prefix_list = ["202.2.0.0", "202.2.0.0", "204.2.0.0", "204.2.0.0"]
data.tg1_vrf2_router_v6_prefix_list = ["3001:1::1", "3001:1::1", "3001:1::1", "3001:1::1"]
data.tg1_vrf1_router_count_list = ["70000","70000","50000","50000"]
data.tg1_vrf1_router_v6_count_list = ['50000', '50000','50000','50000']
data.tg1_vrf2_router_count_list = ["70000","70000","50000", "50000"]
data.tg1_vrf2_router_v6_count_list = ['50000', '50000','50000','50000']
data.tg1_router_prefix_length = "31"
data.tg1_router_v6_prefix_length = "64"

data.tg2_vrf1_ip_addr = ["11.109.104.2", "11.110.104.2"]
data.tg2_vrf1_ipv6_addr = ["fd40:11:109:104::2", "fd40:11:110:104::2"]
data.tg2_vrf2_ip_addr = ["11.109.106.2", "11.110.106.2"]
data.tg2_vrf2_ipv6_addr = ["fd40:11:109:106::2", "fd40:11:110:106::2"]
data.tg2_vrf1_router_prefix = "200.1.0.0"
data.tg2_vrf1_router_v6_prefix = "4000:1::1"
data.tg2_vrf2_router_prefix = "200.2.0.0"
data.tg2_vrf2_router_v6_prefix = "4001:1::1"
data.tg2_router_prefix_length = "32"
data.tg2_router_v6_prefix_length = "64"
data.tg2_router_count = "10000"

data.tg3_vrf1_ip_addr = ["11.61.100.2", "11.62.100.2"]
data.tg3_vrf2_ip_addr = ["11.61.102.2", "11.62.102.2"]
data.tg3_vrf1_router_prefix = "206.1.0.0"
data.tg3_vrf2_router_prefix = "206.2.0.0"
data.tg3_router_prefix_length = "32"
data.tg3_router_count = "10000"

data.tg1_vrf_bgp_as = "4200015158"
data.tg2_vrf_bgp_as = "4200015156"
data.tg3_vrf_bgp_as = "4200015159"
data.dut1_vrf_bgp_as = "4200015155"
data.dut2_vrf_bgp_as = "4200015154"
data.dut3_vrf_bgp_as = "4200015157"

data.dut2_v4_start_ip_addr = ["109.1.0.1","110.2.0.1"]
data.dut2_v6_start_ip_addr = ["109:1::1","110:2::1"]
data.tg2_v4_start_ip_addr = ["109.1.0.2","110.2.0.2"]
data.tg2_v6_start_ip_addr = ["109:1::2","110:2::2"]

data.dut_bfd_timer = "100"
data.tg_bfd_timer = "100"
data.traffic_rate_precent = "99.9"
data.tg_list = []
data.tg_ph_list = []
data.tg1_handle = [0,0,0,0]
data.tg2_handle = [0,0]
data.tg3_handle = [0,0]
data.streams = {}

data.dut_lag = {"PortChannel161":["Ethernet1","Ethernet2"],
                "PortChannel162":["Ethernet3","Ethernet4"]}

## srv6-vpn
data.mysid_prefix = {
    "lsid1":"fd00:201:201::",
    "lsid2":"fd00:201:202::",
    "lsid3":"fd00:201:203::",
    "lsid4":"fd00:201:204::",
    "lsid5":"fd00:201:205::",
    "lsid6":"fd00:201:206::",
    "lsid7":"fd00:201:207::",
    "lsid8":"fd00:201:208::",
    "lsid9":"fd00:201:209::",
    "lsid10":"fd00:201:2010::",
    "lsid11":"fd00:201:2011::",
    "lsid12":"fd00:201:2012::",
    "lsid13":"fd00:201:2013::",
    "lsid14":"fd00:201:2014::",
    "lsid15":"fd00:201:2015::",
    "lsid16":"fd00:201:2016::"
}
data.mysid_base_prefix_len = {"block_len":"32", "node_len":"16", "func_len":"32", "argu_len":"48"}
data.mysid_opcode = {
    "Vrf1":"::fff1:1:0:0:0",
    "Vrf2":"::fff1:2:0:0:0",
    "PRIVATE-TC3":"::fff1:3:0:0:0",
    "PRIVATE-TC4":"::fff1:4:0:0:0",
    "PRIVATE-TC5":"::fff1:5:0:0:0",
    "PRIVATE-TC6":"::fff1:6:0:0:0",
    "PRIVATE-TC7":"::fff1:7:0:0:0",
    "PRIVATE-TC8":"::fff1:8:0:0:0",
    "PRIVATE-TC9":"::fff1:9:0:0:0",
    "PRIVATE-TC10":"::fff1:10:0:0:0",
    "PUBLIC-TC11":"::fff1:11:0:0:0",
    "PUBLIC-TC12":"::fff1:12:0:0:0",
    "PUBLIC-TC13":"::fff1:13:0:0:0",
    "PUBLIC-TC14":"::fff1:14:0:0:0",
    "PUBLIC-TC15":"::fff1:15:0:0:0",
    "PUBLIC-TC16":"::fff1:16:0:0:0",
    "PUBLIC-TC17":"::fff1:17:0:0:0",
    "PUBLIC-TC18":"::fff1:18:0:0:0",
    "PUBLIC-TC19":"::fff1:19:0:0:0",
    "PUBLIC-TC20":"::fff1:20:0:0:0",
    "SX-XIAN-CM-TC21":"::fff1:21:0:0:0",
    "SX-XIAN-CM-TC22":"::fff1:22:0:0:0",
    "SX-XIAN-CM-TC23":"::fff1:23:0:0:0",
    "SX-XIAN-CM-TC24":"::fff1:24:0:0:0",
    "SX-XIAN-CM-TC25":"::fff1:25:0:0:0",
    "SX-XIAN-CM-TC26":"::fff1:26:0:0:0",
    "SX-XIAN-CM-TC27":"::fff1:27:0:0:0",
    "SX-XIAN-CM-TC28":"::fff1:28:0:0:0",
    "SX-XIAN-CM-TC29":"::fff1:29:0:0:0",
    "SX-XIAN-CM-TC30":"::fff1:30:0:0:0",
    "SX-XIAN-CM-TC31":"::fff1:31:0:0:0",
    "SX-XIAN-CM-TC32":"::fff1:32:0:0:0",
    "SX-XIAN-CM-TC33":"::fff1:33:0:0:0",
    "SX-XIAN-CM-TC34":"::fff1:34:0:0:0",
    "SX-XIAN-CM-TC35":"::fff1:35:0:0:0",
    "SX-XIAN-CM-TC36":"::fff1:36:0:0:0",
    "SX-XIAN-CM-TC37":"::fff1:37:0:0:0",
    "SX-XIAN-CM-TC38":"::fff1:38:0:0:0",
    "SX-XIAN-CM-TC39":"::fff1:39:0:0:0",
    "SX-XIAN-CM-TC40":"::fff1:40:0:0:0",
    "ACTN-TC41":"::fff1:41:0:0:0",
    "ACTN-TC42":"::fff1:42:0:0:0",
    "ACTN-TC43":"::fff1:43:0:0:0",
    "ACTN-TC44":"::fff1:44:0:0:0",
    "ACTN-TC45":"::fff1:45:0:0:0",
    "ACTN-TC46":"::fff1:46:0:0:0",
    "ACTN-TC47":"::fff1:47:0:0:0",
    "ACTN-TC48":"::fff1:48:0:0:0",
    "ACTN-TC49":"::fff1:49:0:0:0",
    "ACTN-TC50":"::fff1:50:0:0:0",
    "ACTN-TC51":"::fff1:51:0:0:0",
    "ACTN-TC52":"::fff1:52:0:0:0",
    "ACTN-TC53":"::fff1:53:0:0:0",
    "ACTN-TC54":"::fff1:54:0:0:0",
    "ACTN-TC55":"::fff1:55:0:0:0",
    "ACTN-TC56":"::fff1:56:0:0:0",
    "ACTN-TC57":"::fff1:57:0:0:0",
    "ACTN-TC58":"::fff1:58:0:0:0",
    "ACTN-TC59":"::fff1:59:0:0:0",
    "ACTN-TC60":"::fff1:60:0:0:0",
    "ACTN-TC61":"::fff1:61:0:0:0",
    "ACTN-TC62":"::fff1:62:0:0:0",
    "ACTN-TC63":"::fff1:63:0:0:0",
    "ACTN-TC64":"::fff1:64:0:0:0",
    "VPN1":"::fff2:1:0:0:0",
    "VPN2":"::fff2:2:0:0:0",
    "VPN3":"::fff2:3:0:0:0",
    "VPN4":"::fff2:4:0:0:0",
    "VPN5":"::fff2:5:0:0:0",
    "VPN6":"::fff2:6:0:0:0",
    "VPN7":"::fff2:7:0:0:0",
    "VPN8":"::fff2:8:0:0:0",
    "VPN9":"::fff2:9:0:0:0",
    "VPN10":"::fff2:10:0:0:0",
    "VPN11":"::fff2:11:0:0:0",
    "VPN12":"::fff2:12:0:0:0",
    "VPN13":"::fff2:13:0:0:0",
    "VPN14":"::fff2:14:0:0:0",
    "VPN15":"::fff2:15:0:0:0",
    "VPN16":"::fff2:16:0:0:0",
    "VPN17":"::fff2:17:0:0:0",
    "VPN18":"::fff2:18:0:0:0",
    "VPN19":"::fff2:19:0:0:0",
    "VPN20":"::fff2:20:0:0:0",
    "VPN21":"::fff2:21:0:0:0",
    "VPN22":"::fff2:22:0:0:0",
    "VPN23":"::fff2:23:0:0:0",
    "VPN24":"::fff2:24:0:0:0",
    "VPN25":"::fff2:25:0:0:0",
    "VPN26":"::fff2:26:0:0:0",
    "VPN27":"::fff2:27:0:0:0",
    "VPN28":"::fff2:28:0:0:0",
    "VPN29":"::fff2:29:0:0:0",
    "VPN30":"::fff2:30:0:0:0",
    "VPN31":"::fff2:31:0:0:0",
    "VPN32":"::fff2:32:0:0:0",
    "VPN33":"::fff2:33:0:0:0",
    "VPN34":"::fff2:34:0:0:0",
    "VPN35":"::fff2:35:0:0:0",
    "VPN36":"::fff2:36:0:0:0",
    "VPN37":"::fff2:37:0:0:0",
    "VPN38":"::fff2:38:0:0:0",
    "VPN39":"::fff2:39:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC40":"::fff2:40:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC41":"::fff2:41:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC42":"::fff2:42:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC43":"::fff2:43:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC44":"::fff2:44:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC45":"::fff2:45:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC46":"::fff2:46:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC47":"::fff2:47:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC48":"::fff2:48:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC49":"::fff2:49:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC50":"::fff2:50:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC51":"::fff2:51:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC52":"::fff2:52:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC53":"::fff2:53:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC54":"::fff2:54:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC55":"::fff2:55:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC56":"::fff2:56:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC57":"::fff2:57:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC58":"::fff2:58:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC59":"::fff2:59:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC60":"::fff2:60:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC61":"::fff2:61:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC62":"::fff2:62:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC63":"::fff2:63:0:0:0",
    "ZJ-HANGZHOU-CU-ALIYUN-TC64":"::fff2:64:0:0:0"
}

data.vrf_list = [
    "Vrf1",
    "Vrf2",
    "PRIVATE-TC3",
    "PRIVATE-TC4",
    "PRIVATE-TC5",
    "PRIVATE-TC6",
    "PRIVATE-TC7",
    "PRIVATE-TC8",
    "PRIVATE-TC9",
    "PRIVATE-TC10",
    "PUBLIC-TC11",
    "PUBLIC-TC12",
    "PUBLIC-TC13",
    "PUBLIC-TC14",
    "PUBLIC-TC15",
    "PUBLIC-TC16",
    "PUBLIC-TC17",
    "PUBLIC-TC18",
    "PUBLIC-TC19",
    "PUBLIC-TC20",
    "SX-XIAN-CM-TC21",
    "SX-XIAN-CM-TC22",
    "SX-XIAN-CM-TC23",
    "SX-XIAN-CM-TC24",
    "SX-XIAN-CM-TC25",
    "SX-XIAN-CM-TC26",
    "SX-XIAN-CM-TC27",
    "SX-XIAN-CM-TC28",
    "SX-XIAN-CM-TC29",
    "SX-XIAN-CM-TC30",
    "SX-XIAN-CM-TC31",
    "SX-XIAN-CM-TC32",
    "SX-XIAN-CM-TC33",
    "SX-XIAN-CM-TC34",
    "SX-XIAN-CM-TC35",
    "SX-XIAN-CM-TC36",
    "SX-XIAN-CM-TC37",
    "SX-XIAN-CM-TC38",
    "SX-XIAN-CM-TC39",
    "SX-XIAN-CM-TC40",
    "ACTN-TC41",
    "ACTN-TC42",
    "ACTN-TC43",
    "ACTN-TC44",
    "ACTN-TC45",
    "ACTN-TC46",
    "ACTN-TC47",
    "ACTN-TC48",
    "ACTN-TC49",
    "ACTN-TC50",
    "ACTN-TC51",
    "ACTN-TC52",
    "ACTN-TC53",
    "ACTN-TC54",
    "ACTN-TC55",
    "ACTN-TC56",
    "ACTN-TC57",
    "ACTN-TC58",
    "ACTN-TC59",
    "ACTN-TC60",
    "ACTN-TC61",
    "ACTN-TC62",
    "ACTN-TC63",
    "ACTN-TC64",
    "VPN1",
    "VPN2",
    "VPN3",
    "VPN4",
    "VPN5",
    "VPN6",
    "VPN7",
    "VPN8",
    "VPN9",
    "VPN10",
    "VPN11",
    "VPN12",
    "VPN13",
    "VPN14",
    "VPN15",
    "VPN16",
    "VPN17",
    "VPN18",
    "VPN19",
    "VPN20",
    "VPN21",
    "VPN22",
    "VPN23",
    "VPN24",
    "VPN25",
    "VPN26",
    "VPN27",
    "VPN28",
    "VPN29",
    "VPN30",
    "VPN31",
    "VPN32",
    "VPN33",
    "VPN34",
    "VPN35",
    "VPN36",
    "VPN37",
    "VPN38",
    "VPN39",
    "ZJ-HANGZHOU-CU-ALIYUN-TC40",
    "ZJ-HANGZHOU-CU-ALIYUN-TC41",
    "ZJ-HANGZHOU-CU-ALIYUN-TC42",
    "ZJ-HANGZHOU-CU-ALIYUN-TC43",
    "ZJ-HANGZHOU-CU-ALIYUN-TC44",
    "ZJ-HANGZHOU-CU-ALIYUN-TC45",
    "ZJ-HANGZHOU-CU-ALIYUN-TC46",
    "ZJ-HANGZHOU-CU-ALIYUN-TC47",
    "ZJ-HANGZHOU-CU-ALIYUN-TC48",
    "ZJ-HANGZHOU-CU-ALIYUN-TC49",
    "ZJ-HANGZHOU-CU-ALIYUN-TC50",
    "ZJ-HANGZHOU-CU-ALIYUN-TC51",
    "ZJ-HANGZHOU-CU-ALIYUN-TC52",
    "ZJ-HANGZHOU-CU-ALIYUN-TC53",
    "ZJ-HANGZHOU-CU-ALIYUN-TC54",
    "ZJ-HANGZHOU-CU-ALIYUN-TC55",
    "ZJ-HANGZHOU-CU-ALIYUN-TC56",
    "ZJ-HANGZHOU-CU-ALIYUN-TC57",
    "ZJ-HANGZHOU-CU-ALIYUN-TC58",
    "ZJ-HANGZHOU-CU-ALIYUN-TC59",
    "ZJ-HANGZHOU-CU-ALIYUN-TC60",
    "ZJ-HANGZHOU-CU-ALIYUN-TC61",
    "ZJ-HANGZHOU-CU-ALIYUN-TC62",
    "ZJ-HANGZHOU-CU-ALIYUN-TC63",
    "ZJ-HANGZHOU-CU-ALIYUN-TC64"
]

data.vrf_prefix = {
    "Vrf1":"200.1.19.136/32",
    "Vrf2":"200.2.19.136/32",
    "PRIVATE-TC3":"200.3.19.136/32",
    "PRIVATE-TC4":"200.4.19.136/32",
    "PRIVATE-TC5":"200.5.19.136/32",
    "PRIVATE-TC6":"200.6.19.136/32",
    "PRIVATE-TC7":"200.7.19.136/32",
    "PRIVATE-TC8":"200.8.19.136/32",
    "PRIVATE-TC9":"200.9.19.136/32",
    "PRIVATE-TC10":"200.10.19.136/32",
    "PUBLIC-TC11":"200.11.19.136/32",
    "PUBLIC-TC12":"200.12.19.136/32",
    "PUBLIC-TC13":"200.13.19.136/32",
    "PUBLIC-TC14":"200.14.19.136/32",
    "PUBLIC-TC15":"200.15.19.136/32",
    "PUBLIC-TC16":"200.16.19.136/32",
    "PUBLIC-TC17":"200.17.19.136/32",
    "PUBLIC-TC18":"200.18.19.136/32",
    "PUBLIC-TC19":"200.19.19.136/32",
    "PUBLIC-TC20":"200.20.19.136/32",
    "SX-XIAN-CM-TC21":"200.21.19.136/32",
    "SX-XIAN-CM-TC22":"200.22.19.136/32",
    "SX-XIAN-CM-TC23":"200.23.19.136/32",
    "SX-XIAN-CM-TC24":"200.24.19.136/32",
    "SX-XIAN-CM-TC25":"200.25.19.136/32",
    "SX-XIAN-CM-TC26":"200.26.19.136/32",
    "SX-XIAN-CM-TC27":"200.27.19.136/32",
    "SX-XIAN-CM-TC28":"200.28.19.136/32",
    "SX-XIAN-CM-TC29":"200.29.19.136/32",
    "SX-XIAN-CM-TC30":"200.30.19.136/32",
    "SX-XIAN-CM-TC31":"200.31.19.136/32",
    "SX-XIAN-CM-TC32":"200.32.19.136/32",
    "SX-XIAN-CM-TC33":"200.33.19.136/32",
    "SX-XIAN-CM-TC34":"200.34.19.136/32",
    "SX-XIAN-CM-TC35":"200.35.19.136/32",
    "SX-XIAN-CM-TC36":"200.36.19.136/32",
    "SX-XIAN-CM-TC37":"200.37.19.136/32",
    "SX-XIAN-CM-TC38":"200.38.19.136/32",
    "SX-XIAN-CM-TC39":"200.39.19.136/32",
    "SX-XIAN-CM-TC40":"200.40.19.136/32",
    "ACTN-TC41":"200.41.19.136/32",
    "ACTN-TC42":"200.42.19.136/32",
    "ACTN-TC43":"200.43.19.136/32",
    "ACTN-TC44":"200.44.19.136/32",
    "ACTN-TC45":"200.45.19.136/32",
    "ACTN-TC46":"200.46.19.136/32",
    "ACTN-TC47":"200.47.19.136/32",
    "ACTN-TC48":"200.48.19.136/32",
    "ACTN-TC49":"200.49.19.136/32",
    "ACTN-TC50":"200.50.19.136/32",
    "ACTN-TC51":"201.1.19.136/32",
    "ACTN-TC52":"201.2.19.136/32",
    "ACTN-TC53":"201.3.19.136/32",
    "ACTN-TC54":"201.4.19.136/32",
    "ACTN-TC55":"201.5.19.136/32",
    "ACTN-TC56":"201.6.19.136/32",
    "ACTN-TC57":"201.7.19.136/32",
    "ACTN-TC58":"201.8.19.136/32",
    "ACTN-TC59":"201.9.19.136/32",
    "ACTN-TC60":"201.10.19.136/32",
    "ACTN-TC61":"201.11.19.136/32",
    "ACTN-TC62":"201.12.19.136/32",
    "ACTN-TC63":"201.13.19.136/32",
    "ACTN-TC64":"201.14.19.136/32",
    "VPN1":"201.15.19.136/32",
    "VPN2":"201.16.19.136/32",
    "VPN3":"201.17.19.136/32",
    "VPN4":"201.18.19.136/32",
    "VPN5":"201.19.19.136/32",
    "VPN6":"201.20.19.136/32",
    "VPN7":"201.21.19.136/32",
    "VPN8":"201.22.19.136/32",
    "VPN9":"201.23.19.136/32",
    "VPN10":"201.24.19.136/32",
    "VPN11":"201.25.19.136/32",
    "VPN12":"201.26.19.136/32",
    "VPN13":"201.27.19.136/32",
    "VPN14":"201.28.19.136/32",
    "VPN15":"201.29.19.136/32",
    "VPN16":"201.30.19.136/32",
    "VPN17":"201.31.19.136/32",
    "VPN18":"201.32.19.136/32",
    "VPN19":"201.33.19.136/32",
    "VPN20":"201.34.19.136/32",
    "VPN21":"201.35.19.136/32",
    "VPN22":"201.36.19.136/32",
    "VPN23":"201.37.19.136/32",
    "VPN24":"201.38.19.136/32",
    "VPN25":"201.39.19.136/32",
    "VPN26":"201.40.19.136/32",
    "VPN27":"201.41.19.136/32",
    "VPN28":"201.42.19.136/32",
    "VPN29":"201.43.19.136/32",
    "VPN30":"201.44.19.136/32",
    "VPN31":"201.45.19.136/32",
    "VPN32":"201.46.19.136/32",
    "VPN33":"201.47.19.136/32",
    "VPN34":"201.48.19.136/32",
    "VPN35":"201.49.19.136/32",
    "VPN36":"201.50.19.136/32"
}