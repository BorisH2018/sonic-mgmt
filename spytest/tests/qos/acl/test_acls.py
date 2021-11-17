import pprint
import pytest
import json

from spytest import st, tgapi, SpyTestDict

import apis.switching.vlan as vlan_obj
import apis.qos.acl as acl_obj
import tests.qos.acl.acl_json_config as acl_data
import tests.qos.acl.acl_rules_data as acl_rules_data
import tests.qos.acl.acl_utils as acl_utils
import apis.switching.portchannel as pc_obj
import apis.routing.ip as ipobj
import apis.system.gnmi as gnmiapi
from apis.system.interface import clear_interface_counters,get_interface_counters,show_queue_counters
from apis.system.rest import rest_status
import apis.system.basic as basic_obj
import apis.routing.ip as ip_obj
import apis.routing.arp as arp_obj

from utilities.parallel import ensure_no_exception
import utilities.common as utils

YANG_MODEL = "sonic-acl:sonic-acl"
pp = pprint.PrettyPrinter(indent=4)

vars = dict()
data = SpyTestDict()
data.rate_pps = 100
data.pkts_per_burst = 10
data.tx_timeout = 2
data.TBD = 10
data.portChannelName = "PortChannel1"
data.tg_type = 'ixia'
data.cli_type = ""
data.ipv4_address_D1 = "1.1.1.1"
data.ipv4_address_D2 = "2.2.2.1"
data.ipv4_address_D3 = "100.0.0.1"
data.ipv4_address_D4 = "200.0.0.1"
data.ipv4_portchannel_D1 = "192.168.1.1"
data.ipv4_portchannel_D2 = "192.168.1.2"
data.ipv4_network_D1 = "1.1.1.0/24"
data.ipv4_network_D2 = "2.2.2.0/24"
data.ipv4_network_D3 = "100.0.0.0/24"
data.ipv4_network_D4 = "200.0.0.0/24"
data.ipv6_address_D1 = "1001::1"
data.ipv6_address_D2 = "2001::1"
data.ipv6_address_D3 = "100::1"
data.ipv6_address_D4 = "200::1"
data.ipv6_portchannel_D1 = "3001::1"
data.ipv6_portchannel_D2 = "3001::2"
data.ipv6_network_D1 = "1001::0/64"
data.ipv6_network_D2 = "2001::0/64"
data.ipv6_network_D3 = "100::0/64"
data.ipv6_network_D4 = "200::0/64"

def print_log(msg):
    log_start = "\n================================================================================\n"
    log_end = "\n================================================================================"
    st.log("{} {} {}".format(log_start, msg, log_end))


def get_handles():
    '''
    ######################## Topology ############################

               +---------+                  +-------+
               |         +------------------+       |
      TG1 -----|  DUT1   |  portchannel     |  DUT2 +----- TG2
               |         +------------------+       |
               +---------+                  +-------+

    ##############################################################
    '''
    global vars, tg_port_list
    vars = st.ensure_min_topology("D1D2:2", "D1T1:2", "D2T1:2")
    tg1, tg_ph_1 = tgapi.get_handle_byname("T1D1P1")
    tg2, tg_ph_2 = tgapi.get_handle_byname("T1D2P1")
    tg3, tg_ph_3 = tgapi.get_handle_byname("T1D1P2")
    tg4, tg_ph_4 = tgapi.get_handle_byname("T1D2P2")
    if tg1.tg_type == 'stc': data.tg_type = 'stc'
    tg_port_list = [tg_ph_1, tg_ph_2, tg_ph_3]
    tg1.tg_traffic_control(action="reset", port_handle=tg_ph_1)
    tg2.tg_traffic_control(action="reset", port_handle=tg_ph_2)
    tg3.tg_traffic_control(action="reset", port_handle=tg_ph_3)
    tg4.tg_traffic_control(action="reset", port_handle=tg_ph_4)
    return (tg1, tg2, tg3, tg4, tg_ph_1, tg_ph_2, tg_ph_3, tg_ph_4)



def apply_module_configuration():
    print_log("Applying module configuration")

    data.dut1_lag_members = [vars.D1D2P1, vars.D1D2P2]
    data.dut2_lag_members = [vars.D2D1P1, vars.D2D1P2]

    # create portchannel
    utils.exec_all(True, [
        utils.ExecAllFunc(pc_obj.create_portchannel, vars.D1, data.portChannelName),
        utils.ExecAllFunc(pc_obj.create_portchannel, vars.D2, data.portChannelName),
    ])

    # add portchannel members
    utils.exec_all(True, [
        utils.ExecAllFunc(pc_obj.add_portchannel_member, vars.D1, data.portChannelName, data.dut1_lag_members),
        utils.ExecAllFunc(pc_obj.add_portchannel_member, vars.D2, data.portChannelName, data.dut2_lag_members),
    ])



def clear_module_configuration():
    print_log("Clearing module configuration")
    # delete Ipv4 address
    print_log("Delete ip address configuration:")
    ip_obj.clear_ip_configuration([vars.D1, vars.D2], family='ipv4')
    # delete Ipv6 address
    ip_obj.clear_ip_configuration([vars.D1, vars.D2], family='ipv6')
    # delete ipv4 static routes
    ip_obj.delete_static_route(vars.D1, data.ipv4_portchannel_D2, data.ipv4_network_D2, shell="vtysh",
                               family="ipv4")
    ip_obj.delete_static_route(vars.D1, data.ipv4_portchannel_D2, "200.0.0.0/24", shell="vtysh",
                               family="ipv4")
    ip_obj.delete_static_route(vars.D2, data.ipv4_portchannel_D1, data.ipv4_network_D1, shell="vtysh",
                               family="ipv4")
    # delete ipv6 static routes
    ip_obj.delete_static_route(vars.D1, data.ipv6_portchannel_D2, data.ipv6_network_D2, shell="vtysh",
                               family="ipv6")
    ip_obj.delete_static_route(vars.D2, data.ipv6_portchannel_D1, data.ipv6_network_D1, shell="vtysh",
                               family="ipv6")

    # delete portchannel members
    utils.exec_all(True, [
        utils.ExecAllFunc(pc_obj.delete_portchannel_member, vars.D1, data.portChannelName, data.dut1_lag_members),
        utils.ExecAllFunc(pc_obj.delete_portchannel_member, vars.D2, data.portChannelName, data.dut2_lag_members),
    ])
    # delete portchannel
    utils.exec_all(True, [
        utils.ExecAllFunc(pc_obj.delete_portchannel, vars.D1, data.portChannelName),
        utils.ExecAllFunc(pc_obj.delete_portchannel, vars.D2, data.portChannelName),
    ])

    [_, exceptions] = utils.exec_all(True, [[acl_obj.acl_delete, vars.D1], [acl_obj.acl_delete, vars.D2]])

    #Clear static arp entries
    print_log("Clearing ARP entries")
    arp_obj.clear_arp_table(vars.D1)
    arp_obj.clear_arp_table(vars.D2)
    #Clear static ndp entries
    print_log("Clearing NDP entries")
    arp_obj.clear_ndp_table(vars.D1)
    arp_obj.clear_ndp_table(vars.D2)


def add_port_to_acl_table(config, table_name, port):
    config['ACL_TABLE'][table_name]['ports'] = []
    config['ACL_TABLE'][table_name]['ports'].append(port)


def change_acl_rules(config, rule_name, attribute, value):
    config["ACL_RULE"][rule_name][attribute] = value


def apply_acl_config(dut, config):
    json_config = json.dumps(config)
    json.loads(json_config)
    st.apply_json2(dut, json_config)


def create_streams(tx_tg, rx_tg, rules, match, mac_src, mac_dst,dscp=None):
    # use the ACL rule definitions to create match/non-match traffic streams
    # instead of hardcoding the traffic streams
    my_args = {
        'port_handle': data.tgmap[tx_tg]['handle'], 'mode': 'create', 'frame_size': '128',
        'transmit_mode': 'continuous', 'length_mode': 'fixed',
        'l2_encap': 'ethernet_ii_vlan', 'duration': '1',
        'rate_pps': data.rate_pps,
        'high_speed_result_analysis': 0, 'mac_src': mac_src, 'mac_dst': mac_dst,
        'port_handle2': data.tgmap[rx_tg]['handle']
    }
    if dscp:
        my_args.update({"ip_dscp": dscp})

    for rule, attributes in rules.items():
        if ("IP_TYPE" in attributes) or ("ETHER_TYPE" in attributes):
            continue
        if match in rule:
            params = {}
            tmp = dict(my_args)
            for key, value in attributes.items():
                params.update(acl_utils.get_args_l3(key, value, attributes, data.rate_pps, data.tg_type))
            tmp.update(params)
            stream = data.tgmap[tx_tg]['tg'].tg_traffic_config(**tmp)
            stream_id = stream['stream_id']
            s = {}
            s[stream_id] = attributes
            s[stream_id]['TABLE'] = rule
            data.tgmap[tx_tg]['streams'].update(s)

def create_streams_for_qos(tx_tg, rx_tg, rules, match, mac_src, mac_dst):
    # use the ACL rule definitions to create match/non-match traffic streams
    # instead of hardcoding the traffic streams
    my_args = {
        'port_handle': data.tgmap[tx_tg]['handle'], 'mode': 'create', 'frame_size': '128',
        'transmit_mode': 'continuous', 'length_mode': 'fixed',
        'l2_encap': 'ethernet_ii_vlan', 'duration': '1',
        'rate_pps': data.rate_pps,
        'high_speed_result_analysis': 0, 'mac_src': mac_src, 'mac_dst': mac_dst,
        'port_handle2': data.tgmap[rx_tg]['handle']
    }

    for rule, attributes in rules.items():
        if ("IP_TYPE" in attributes) or ("ETHER_TYPE" in attributes):
            continue
        if match in rule:
            params = {}
            tmpv4 = dict(my_args)
            tmpv6 = tmpv4.copy()
            for key, value in attributes.items():
                params.update(acl_utils.get_args_l3(key, value, attributes, data.rate_pps, data.tg_type))
            # ipv4 + ipv6
            tmpv4.update(params)
            tmpv6.update(params)

            v4 = {'ip_src_addr':'100.0.0.2', 'ip_dst_addr':'200.0.0.2', 'l3_protocol':'ipv4', 'ip_dst_mode':"fixed", "ip_src_mode":"fixed"}
            tmpv4.update(v4)
            v6 = {'ipv6_src_addr':'100::2', 'ipv6_dst_addr':'200::2', 'l3_protocol':'ipv6', 'ipv6_dst_mode':"fixed", "ipv6_src_mode":"fixed"}
            if tmpv6.has_key('ip_dscp'):
                dscp = tmpv6['ip_dscp']
                tmpv6.pop('ip_dscp')
                tmpv6.update({'ipv6_traffic_class':dscp*4})
            tmpv6.update(v6)
            streamv4 = data.tgmap[tx_tg]['tg'].tg_traffic_config(**tmpv4)
            stream_id4 = streamv4['stream_id']
            streamv6 = data.tgmap[tx_tg]['tg'].tg_traffic_config(**tmpv6)
            stream_id6 = streamv6['stream_id']
            s = {}
            s[stream_id4] = attributes
            s[stream_id4]['TABLE'] = rule
            data.tgmap[tx_tg]['streams'].update(s)
            s = {}
            s[stream_id6] = attributes
            s[stream_id6]['TABLE'] = rule
            data.tgmap[tx_tg]['streams'].update(s)

def transmit(tg):
    print_log("Transmitting streams")
    data.tgmap[tg]['tg'].tg_traffic_control(action='clear_stats', port_handle=tg_port_list)
    data.tgmap[tg]['tg'].tg_traffic_control(action='run', stream_handle = list(data.tgmap[tg]['streams'].keys()),
                                            duration=1)


def verify_acl_hit_counters(dut, table_name, acl_type="ip"):
    result = True
    acl_rule_counters = acl_obj.show_acl_counters(dut, acl_table=table_name, acl_type=acl_type)
    for rule in acl_rule_counters:
        if not rule['packetscnt'] or rule['packetscnt'] == 0:
            return False
    return result


def verify_packet_count(tx, tx_port, rx, rx_port, table):
    result = True
    tg_tx = data.tgmap[tx]
    tg_rx = data.tgmap[rx]
    exp_ratio = 0
    #action = "DROP"
    attr_list = []
    traffic_details = dict()
    action_list = []
    index = 0
    for s_id, attr in tg_tx['streams'].items():
        if table in attr['TABLE']:
            index = index + 1
            if attr["PACKET_ACTION"] == "FORWARD" or "QUEUE" in attr["PACKET_ACTION"] or "REMARK-DSCP" in attr["PACKET_ACTION"]:
                exp_ratio = 1
                action = "FORWARD"
            else:
                exp_ratio = 0
                action = "DROP"
            traffic_details[str(index)] = {
                    'tx_ports': [tx_port],
                    'tx_obj': [tg_tx["tg"]],
                    'exp_ratio': [exp_ratio],
                    'rx_ports': [rx_port],
                    'rx_obj': [tg_rx["tg"]],
                    'stream_list': [[s_id]]
                }
            attr_list.append(attr)
            action_list.append(action)
    result_all = tgapi.validate_tgen_traffic(traffic_details=traffic_details, mode='streamblock',
                                    comp_type='packet_count', return_all=1, delay_factor=1, retry=1)
    for result1, action, attr in zip(result_all[1], action_list, attr_list):
        result = result and result1
        if result1:
            if action == "FORWARD":
                msg = "Traffic successfully forwarded for the rule: {}".format(json.dumps(attr))
                print_log(msg)
            else:
                msg = "Traffic successfully dropped for the rule: {}".format(json.dumps(attr))
                print_log(msg)
        else:
            if action == "FORWARD":
                msg = "Traffic failed to forward for the rule: {}".format(json.dumps(attr))
                print_log(msg)
            else:
                msg = "Traffic failed to drop for the rule: {}".format(json.dumps(attr))
                print_log(msg)
    return result


def initialize_topology():
    print_log("Initializing Topology")
    (tg1, tg2, tg3, tg4, tg_ph_1, tg_ph_2, tg_ph_3, tg_ph_4) = get_handles()
    data.tgmap = {
        "tg1": {
            "tg": tg1,
            "handle": tg_ph_1,
            "streams": {}
        },
        "tg2": {
            "tg": tg2,
            "handle": tg_ph_2,
            "streams": {}
        },
        "tg3": {
            "tg": tg3,
            "handle": tg_ph_3,
            "streams": {}
        },
        "tg4": {
            "tg": tg4,
            "handle": tg_ph_4,
            "streams": {}
        }
    }
    data.vars = vars

@pytest.fixture(scope="module", autouse=True)
def acl_v4_module_hooks(request):
    # initialize topology
    initialize_topology()

    # apply module configuration
    apply_module_configuration()

    acl_config1 = acl_data.acl_json_config_d1
    add_port_to_acl_table(acl_config1, 'L3_IPV4_INGRESS', vars.D1T1P1)
    add_port_to_acl_table(acl_config1, 'L3_IPV4_EGRESS', vars.D1T1P1)
    acl_config2 = acl_data.acl_json_config_d2
    add_port_to_acl_table(acl_config2, 'L3_IPV6_INGRESS', vars.D2T1P1)
    add_port_to_acl_table(acl_config2, 'L3_IPV6_EGRESS', vars.D2T1P1)
    acl_config3 = acl_data.acl_json_config_qos
    add_port_to_acl_table(acl_config3, 'QOS', vars.D1T1P2)
    acl_config4 = acl_data.acl_json_config_egress_qos_dscp
    add_port_to_acl_table(acl_config4, 'L3_IPV6_DSCP_EGRESS', vars.D2T1P2)
    add_port_to_acl_table(acl_config4, 'L3_IPV4_DSCP_EGRESS', vars.D2T1P2)

    print_log('Creating ACL tables and rules')
    utils.exec_all(True, [
        utils.ExecAllFunc(acl_obj.apply_acl_config, vars.D1, acl_config1),
        utils.ExecAllFunc(acl_obj.apply_acl_config, vars.D2, acl_config2),
    ])

    utils.exec_all(True, [
        utils.ExecAllFunc(acl_obj.apply_acl_config, vars.D1, acl_config3),
        utils.ExecAllFunc(acl_obj.apply_acl_config, vars.D2, acl_config4),
    ])
    # create streams
    data.mac1 = basic_obj.get_ifconfig_ether(vars.D1, vars.D1T1P1)
    data.mac2 = basic_obj.get_ifconfig_ether(vars.D2, vars.D2T1P1)

    print_log('Creating streams')
    create_streams("tg1", "tg2", acl_config1['ACL_RULE'], "L3_IPV4_INGRESS", \
                   mac_src="00:0a:01:00:00:01", mac_dst=data.mac1, dscp=62)
    create_streams("tg1", "tg2", acl_config2['ACL_RULE'], "L3_IPV6_EGRESS", \
                   mac_src="00:0a:01:00:00:01", mac_dst=data.mac1)
    create_streams("tg2", "tg1", acl_config2['ACL_RULE'], "L3_IPV6_INGRESS", \
                   mac_src="00:0a:01:00:11:02", mac_dst=data.mac2)
    create_streams("tg2", "tg1", acl_config1['ACL_RULE'], "L3_IPV4_EGRESS", \
                   mac_src="00:0a:01:00:11:02", mac_dst=data.mac2, dscp=61)

    create_streams_for_qos("tg3", "tg4", acl_config3['ACL_RULE'], "QOS", \
                   mac_src="00:0a:01:00:00:01", mac_dst=data.mac1)

    print_log('Completed module configuration')

    st.log("Configuring ipv4 address on ixia connected interfaces and portchannels present on both the DUTs")
    ip_obj.config_ip_addr_interface(vars.D1, vars.D1T1P1, data.ipv4_address_D1, 24, family="ipv4", config='add')
    ip_obj.config_ip_addr_interface(vars.D2, vars.D2T1P1, data.ipv4_address_D2, 24, family="ipv4", config='add')
    ip_obj.config_ip_addr_interface(vars.D1, vars.D1T1P2, data.ipv4_address_D3, 24, family="ipv4", config='add')
    ip_obj.config_ip_addr_interface(vars.D2, vars.D2T1P2, data.ipv4_address_D4, 24, family="ipv4", config='add')

    ip_obj.config_ip_addr_interface(vars.D1, data.portChannelName, data.ipv4_portchannel_D1, 24, family="ipv4",
                                    config='add')
    ip_obj.config_ip_addr_interface(vars.D2, data.portChannelName, data.ipv4_portchannel_D2, 24, family="ipv4",
                                    config='add')

    st.log("Configuring ipv6 address on ixia connected interfaces and portchannels present on both the DUTs")
    ip_obj.config_ip_addr_interface(vars.D1, vars.D1T1P1, data.ipv6_address_D1, 64, family="ipv6", config='add')
    ip_obj.config_ip_addr_interface(vars.D2, vars.D2T1P1, data.ipv6_address_D2, 64, family="ipv6", config='add')
    ip_obj.config_ip_addr_interface(vars.D1, vars.D1T1P2, data.ipv6_address_D3, 64, family="ipv6", config='add')
    ip_obj.config_ip_addr_interface(vars.D2, vars.D2T1P2, data.ipv6_address_D4, 64, family="ipv6", config='add')

    ip_obj.config_ip_addr_interface(vars.D1, data.portChannelName, data.ipv6_portchannel_D1, 64, family="ipv6",
                                    config='add')
    ip_obj.config_ip_addr_interface(vars.D2, data.portChannelName, data.ipv6_portchannel_D2, 64, family="ipv6",
                                    config='add')

    st.log("configuring ipv4 static routes on both the DUTs")
    ip_obj.create_static_route(vars.D1, data.ipv4_portchannel_D2, data.ipv4_network_D2, shell="vtysh",
                               family="ipv4")
    ip_obj.create_static_route(vars.D1, data.ipv4_portchannel_D2, data.ipv4_network_D4, shell="vtysh",
                               family="ipv4")
    ip_obj.create_static_route(vars.D2, data.ipv4_portchannel_D1, data.ipv4_network_D1, shell="vtysh",
                               family="ipv4")
    ip_obj.create_static_route(vars.D2, data.ipv4_portchannel_D1, data.ipv4_network_D3, shell="vtysh",
                               family="ipv4")

    st.log("configuring ipv6 static routes on both the DUTs")
    ip_obj.create_static_route(vars.D1, data.ipv6_portchannel_D2, data.ipv6_network_D2, shell="vtysh",
                               family="ipv6")
    ip_obj.create_static_route(vars.D1, data.ipv6_portchannel_D2, data.ipv6_network_D4, shell="vtysh",
                               family="ipv6")
    ip_obj.create_static_route(vars.D2, data.ipv6_portchannel_D1, data.ipv6_network_D1, shell="vtysh",
                               family="ipv6")
    ip_obj.create_static_route(vars.D2, data.ipv6_portchannel_D1, data.ipv6_network_D3, shell="vtysh",
                               family="ipv6")

    st.log("configuring static arp entries")
    arp_obj.add_static_arp(vars.D1, "1.1.1.2", "00:0a:01:00:00:01", vars.D1T1P1)
    arp_obj.add_static_arp(vars.D2, "2.2.2.2", "00:0a:01:00:11:02", vars.D2T1P1)
    arp_obj.add_static_arp(vars.D2, "2.2.2.4", "00:0a:01:00:11:02", vars.D2T1P1)
    arp_obj.add_static_arp(vars.D1, "1.1.1.4", "00:0a:01:00:00:01", vars.D1T1P1)
    arp_obj.add_static_arp(vars.D2, "2.2.2.5", "00:0a:01:00:11:02", vars.D2T1P1)
    arp_obj.add_static_arp(vars.D1, "1.1.1.5", "00:0a:01:00:00:01", vars.D1T1P1)
    arp_obj.add_static_arp(vars.D2, "2.2.2.6", "00:0a:01:00:11:02", vars.D2T1P1)
    arp_obj.add_static_arp(vars.D1, "1.1.1.6", "00:0a:01:00:00:01", vars.D1T1P1)

    arp_obj.add_static_arp(vars.D2, "200.0.0.2", "00:0a:01:00:11:03", vars.D2T1P2)
    arp_obj.show_arp(vars.D1)
    arp_obj.show_arp(vars.D2)

    st.log("configuring static ndp entries")
    arp_obj.config_static_ndp(vars.D1, "1001::2", "00:0a:01:00:00:01", vars.D1T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D2, "2001::2", "00:0a:01:00:11:02", vars.D2T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D1, "1001::4", "00:0a:01:00:00:01", vars.D1T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D2, "2001::4", "00:0a:01:00:11:02", vars.D2T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D1, "1001::5", "00:0a:01:00:00:01", vars.D1T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D2, "2001::5", "00:0a:01:00:11:02", vars.D2T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D1, "1001::6", "00:0a:01:00:00:01", vars.D1T1P1, operation="add")
    arp_obj.config_static_ndp(vars.D2, "2001::6", "00:0a:01:00:11:02", vars.D2T1P1, operation="add")

    arp_obj.config_static_ndp(vars.D2, "200::2", "00:0a:01:00:11:03", vars.D2T1P2, operation="add")

    arp_obj.show_ndp(vars.D1)
    arp_obj.show_ndp(vars.D2)

    yield
    clear_module_configuration()

@pytest.fixture(scope="function", autouse=True)
def acl_function_hooks(request):
    yield
    if st.get_func_name(request) == "test_ft_acl_ingress_ipv4":
        acl_obj.delete_acl_table(vars.D1, acl_type="ip", acl_table_name=['L3_IPV4_INGRESS'])
    elif st.get_func_name(request) == "test_ft_acl_egress_ipv6":
        acl_obj.delete_acl_table(vars.D2, acl_type="ipv6", acl_table_name=['L3_IPV6_EGRESS'])
    elif st.get_func_name(request) == "test_ft_acl_qos":
        acl_obj.delete_acl_table(vars.D1, acl_type="ip", acl_table_name=['QOS'])
        acl_obj.delete_acl_table(vars.D2, acl_type="ip", acl_table_name=['L3_IPV4_DSCP_EGRESS'])
        acl_obj.delete_acl_table(vars.D2, acl_type="ipv6", acl_table_name=['L3_IPV6_DSCP_EGRESS'])


def verify_rule_priority(dut, table_name, acl_type="ip"):
    acl_rule_counters = acl_obj.show_acl_counters(dut, acl_table=table_name, acl_rule='PermitAny7', acl_type=acl_type)
    if len(acl_rule_counters) == 1:
        if (int(acl_rule_counters[0]['packetscnt']) != 0):
            print_log("ACL Rule priority test failed")
            return False
        else:
            return True
    else:
        return True

def verify_queue_counters_pps_match(dut, port, q, expect):
    counter = show_queue_counters(dut, port, queue='UC{}'.format(q))
    if (counter[0]['pkts_count'] >= expect):
        return True
    return False

@pytest.mark.acl_test345654
def test_ft_acl_ingress_ipv4():
    '''
    IPv4 Ingress ACL is applied on DUT1 port connected to TG Port#1
    Traffic is sent on TG Port #1
    Traffic is recieved at TG Port #2
    '''
    [_, exceptions] = utils.exec_all(True, [[acl_obj.clear_acl_counter, vars.D1], [acl_obj.clear_acl_counter, vars.D2]])
    ensure_no_exception(exceptions)
    transmit('tg1')
    result1 = verify_packet_count('tg1', vars.T1D1P1, 'tg2', vars.T1D2P1, "L3_IPV4_INGRESS")

    print_log('Verifing IPv4 Ingress ACL hit counters')
    result2 = verify_acl_hit_counters(vars.D1, "L3_IPV4_INGRESS")
    result3 = verify_rule_priority(vars.D1, "L3_IPV4_INGRESS")

    acl_utils.report_result(result1 and result2 and result3 )

@pytest.mark.acl_test345654
def test_ft_acl_qos():
    transmit('tg3')
    result1 = verify_packet_count('tg3', vars.T1D1P2, 'tg4', vars.T1D2P2, "QOS")
    result2 = verify_acl_hit_counters(vars.D1, "QOS")
    result3 = verify_acl_hit_counters(vars.D2, "L3_IPV6_DSCP_EGRESS", acl_type="ipv6")
    result4 = verify_acl_hit_counters(vars.D2, "L3_IPV4_DSCP_EGRESS")
    counter1 = show_queue_counters(vars.D1, vars.D1D2P1, queue='UC5')
    counter2 = show_queue_counters(vars.D1, vars.D1D2P2, queue='UC5')
    if counter1 + counter2 < 200:
        st.report_fail("Check queue counter failed!");

    acl_utils.report_result(result1 and result2 and result3 and result4)

#@pytest.mark.acl_test
#def test_ft_acl_egress_ipv4():
#    '''
#    IPv4 Egress ACL is applied on DUT1 port connected to TG Port#1
#    Traffic is sent on TG Port #2
#    Traffic is recieved at TG Port #1
#    '''
#    transmit('tg2')
#    result1 = verify_packet_count('tg2', vars.T1D2P1, 'tg1', vars.T1D1P1, "L3_IPV4_EGRESS")
#    print_log('Verifing IPv4 Egress ACL hit counters')
#    result2 = verify_acl_hit_counters(vars.D1, "L3_IPV4_EGRESS")
#    acl_utils.report_result(result1 and result2)
#
#
#@pytest.mark.acl_test678
#def test_ft_acl_egress_ipv6():
#    '''
#    IPv6 Egress ACL is applied on DUT2 port connected to TG Port #2
#    Traffic is sent on TG Port #1
#    Traffic is recieved at TG Port #2
#    '''
#    [_, exceptions] = utils.exec_all(True, [[clear_interface_counters, vars.D1], [clear_interface_counters, vars.D2]])
#    ensure_no_exception(exceptions)
#    [_, exceptions] = utils.exec_all(True, [[get_interface_counters, vars.D1, vars.D1T1P1],
#                                           [get_interface_counters, vars.D2, vars.D2T1P1]])
#    ensure_no_exception(exceptions)
#    [_, exceptions] = utils.exec_all(True, [[acl_obj.clear_acl_counter, vars.D1], [acl_obj.clear_acl_counter, vars.D2]])
#    transmit('tg1')
#    [_, exceptions] = utils.exec_all(True, [[get_interface_counters, vars.D1, vars.D1T1P1],
#                                           [get_interface_counters, vars.D2, vars.D2T1P1]])
#    ensure_no_exception(exceptions)
#    result1 = verify_packet_count('tg1', vars.T1D1P1, 'tg2', vars.T1D2P1, "L3_IPV6_EGRESS")
#    print_log('Verifing IPv6 Egress ACL hit counters')
#    result2 = verify_acl_hit_counters(vars.D2, "L3_IPV6_EGRESS", acl_type="ipv6")
#    acl_utils.report_result(result1 and result2)
#
#
#@pytest.mark.community
#@pytest.mark.community_fail
#def test_ft_acl_ingress_ipv6():
#    '''
#    IPv6 Ingress ACL is applied on DUT2 port connected to TG Port #2
#    Traffic is sent on TG Port #2
#    Traffic is recieved at TG Port #1
#    '''
#    [_, exceptions] = utils.exec_all(True, [[clear_interface_counters, vars.D1], [clear_interface_counters, vars.D2]])
#    ensure_no_exception(exceptions)
#    [_, exceptions] = utils.exec_all(True, [[get_interface_counters, vars.D1, vars.D1T1P1],
#                                           [get_interface_counters, vars.D2, vars.D2T1P1]])
#    ensure_no_exception(exceptions)
#    transmit('tg2')
#    [_, exceptions] = utils.exec_all(True, [[get_interface_counters, vars.D1, vars.D1T1P1],
#                                           [get_interface_counters, vars.D2, vars.D2T1P1]])
#    ensure_no_exception(exceptions)
#    result1 = verify_packet_count('tg2', vars.T1D2P1, 'tg1', vars.T1D1P1, "L3_IPV6_INGRESS")
#    print_log('Verifing IPv6 Ingress ACL hit counters')
#
#    result2 = verify_acl_hit_counters(vars.D2, "L3_IPV6_INGRESS", acl_type="ipv6")
#    result3 = verify_rule_priority(vars.D2, "L3_IPV6_INGRESS", acl_type="ipv6")
#    acl_utils.report_result(result1 and result2 and result3)
#
#
