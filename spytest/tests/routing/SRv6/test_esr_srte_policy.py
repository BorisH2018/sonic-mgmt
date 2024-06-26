import os
import pytest
from spytest import st

import matplotlib
matplotlib.use('Agg')

from utilities.utils import retry_api

from esr_vars import * #all the variables used for vrf testcase
from esr_vars import data
from esr_lib import *
from ixia_vars import *
from ixia_helper import *

dut1 = 'MC-58'
dut2 = 'MC-59'
data.my_dut_list = [dut1, dut2]
data.load_policy_ixia_conf_done = False
data.dut1_load_2k_policy_config_done = False
data.dut2_load_1k_policy_config_done = False
data.dut2_load_2k_policy_config_done = False
data.dut2_load_4k_policy_config_done = False
data.traffic_1k_te_policy = False
data.traffic_2k_te_policy = False


@pytest.fixture(scope="module", autouse=True)
def esr_srte_policy_module_hooks(request):
    try:
        ixia_controller_init()
        yield
    except Exception as e:
        st.log("Exception occurred: {}".format(e))
    finally:
        ixia_stop_all_protocols()
        ixia_controller_deinit()

@pytest.fixture(scope="function", autouse=True)
def esr_srte_policy_func_hooks(request):
    func_name = st.get_func_name(request)
    st.log("esr_srte_policy_func_hooks enter {}".format(func_name))
    if func_name == 'test_srte_policy_2k_vrf_ipv4_ipv6_07':
        double_dut_load_config('ip_ipv6_2k_config', 'ip_ipv6_2k_config')
        ixia_load_config(ESR_IPV4_IPV6_POLICY_CONFIG)
        ixia_start_all_protocols()
        st.wait(60)
    else:
        if data.dut1_load_2k_policy_config_done == False:
            double_dut_load_config('2k_config', '1k_config')
            data.dut1_load_2k_policy_config_done = True
            data.dut2_load_1k_policy_config_done = True

        if data.load_policy_ixia_conf_done == False:
            ixia_load_config(ESR_2K_POLICY_CONFIG)
            ixia_start_all_protocols()
            st.wait(60)
            data.load_policy_ixia_conf_done = True

    yield
    if func_name != 'test_srte_policy_2k_vrf_ipv4_ipv6_07':
        if data.traffic_1k_te_policy == True:
            ixia_stop_traffic(TRAFFIC_1K_TE_POLICY)
            data.traffic_1k_te_policy == False
        if data.traffic_2k_te_policy == True:
            ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
            data.traffic_2k_te_policy == False
    pass

def load_config(duts, filesuffix1, filesuffix2):
    curr_path = os.getcwd()
    method="replace_configdb"
    for dut in duts:
        if (dut == "MC-58"):
            json_file = "{}/routing/SRv6/esr_te_dut1_{}.json".format(curr_path, filesuffix1)
        else:
            json_file = "{}/routing/SRv6/esr_te_dut2_{}.json".format(curr_path, filesuffix2)
        try:
            st.apply_files(dut, [json_file], method=method)
        except Exception as e:
            print("Error applying config file {} to {}: {}".format(json_file, dut, e))
            return

        st.wait(10)

    try:
        st.reboot(duts)
    except Exception as e:
        print("Error rebooting {}: {}".format(duts, e))
        return
    st.banner("{} json config loaded completed for {}".format(filesuffix1, duts))


def dut_load_config(dut, filesuffix):
    curr_path = os.getcwd()

    json_file_dut_multi_vrf = curr_path+"/routing/SRv6/"+filesuffix+".json"
    st.apply_files(dut, [json_file_dut_multi_vrf], method="replace_configdb")

    st.wait(10)

    st.reboot([dut])

    st.banner("%s json config loaded completed" % (filesuffix))

def double_dut_load_config(filesuffix1, filesuffix2):
    load_config([dut1, dut2], filesuffix1, filesuffix2)

'''
1. Dut1/Dut2 config 1k vrfs and 1k policy 
2. Each policy has 4 different priority cpaths
3. Each policy has a sbfd to detect
4. Shutdown/no shutdown interface on Dut1, sbfd flap
5. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_1k_policy_01():

    if data.dut2_load_1k_policy_config_done == False:
        st.log("esr_srte_policy_func_hooks enter test_srte_policy_2k_vrf_1k_policy_01")
        dut_load_config(dut2, "esr_te_dut2_1k_config")
        data.dut2_load_1k_policy_config_done = True
        data.dut2_load_2k_policy_config_done = False
        data.dut2_load_4k_policy_config_done = False

    if not retry_api(check_bgp_state, dut2, "2000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp state failed")
    st.wait(5)

    ixia_disable_traffic(TRAFFIC_2K_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_1K_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_1K_TE_POLICY)
    if not ret:
        st.report_fail("Step1: Start traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    data.traffic_1k_te_policy = True
    st.wait(30)
    #check traffic cpath d, on interface Ethernet4
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step2: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step3: The cpath d: bfd-name d not down")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet3"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step4: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n no shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step5: The cpath d: bfd-name d not up")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step6: Check dut interface counters failed")

    ret = ixia_stop_traffic(TRAFFIC_1K_TE_POLICY)
    if not ret:
        st.report_fail("Step7: Stop traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))

    #check Tx Frame Rate
    ret = ixia_check_traffic(TRAFFIC_1K_TE_POLICY, key="Rx Frame Rate", value=100000, exact_match = False)
    if not ret:
        st.report_fail("Step8: Check traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    data.traffic_1k_te_policy = True
    ret = ixia_stop_traffic(TRAFFIC_1K_TE_POLICY)
    if not ret:
        st.report_fail("Step9: Stop traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    data.traffic_1k_te_policy = False
    st.report_pass("test_case_passed")

'''
1. Dut1/Dut2 config 1k vrfs and 1k color only 
2. Each policy has 4 different priority cpaths
3. Each policy has a sbfd to detect
4. Shutdown/no shutdown interface on Dut1, sbfd flap
5. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_1k_policy_color_only_02():

    if data.dut2_load_1k_policy_config_done == False:
        st.log("esr_srte_policy_func_hooks enter test_srte_policy_2k_vrf_1k_policy_color_only_02")
        dut_load_config(dut2, "esr_te_dut2_1k_config")
        data.dut2_load_1k_policy_config_done = True
        data.dut2_load_2k_policy_config_done = False
        data.dut2_load_4k_policy_config_done = False

    del_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "no neighbor 2000::179 activate"'
    st.config(dut1, del_neighbor)
    st.wait(5)

    add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 1000::179 activate"'
    st.config(dut1, add_neighbor)
    st.wait(30)

    if not retry_api(check_bgp_state, dut2, "1000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp state failed")
    st.wait(5)

    ixia_disable_traffic(TRAFFIC_2K_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_1K_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_1K_TE_POLICY)
    data.traffic_1k_te_policy = True
    if not ret:
        st.report_fail("Step1: Start traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    st.wait(30)
    #check traffic cpath d, on interface Ethernet4
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step2: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step4: The cpath d: bfd-name d not down")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet3"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step5: Check dut interface counters failed")

    #shutdown Ethernet3
    cmd = "interface {}\n shutdown\n".format("Ethernet3")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name c"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step6: The cpath c: bfd-name c not down")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet2"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step7: Check dut interface counters failed")

    #shutdown Ethernet2
    cmd = "interface {}\n shutdown\n".format("Ethernet2")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name b"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step8: The cpath b: bfd-name b not down")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet1"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step9: Check dut interface counters failed")
    st.wait(10)
    #no shutdown Ethernet2
    cmd = "interface {}\n no shutdown\n".format("Ethernet2")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name b"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step10: The cpath b: bfd-name b not up")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet2"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step11: Check dut interface counters failed")

    #no shutdown Ethernet3
    cmd = "interface {}\n no shutdown\n".format("Ethernet3")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name c"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step12: The cpath c: bfd-name c not down")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet3"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step13: Check dut interface counters failed")

    #no shutdown Ethernet4
    cmd = "interface {}\n no shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step14: The cpath d: bfd-name d not down")

    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 150, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step15: Check dut interface counters failed")
    
    ret = ixia_stop_traffic(TRAFFIC_1K_TE_POLICY)
    if not ret:
        st.report_fail("Step16: Stop traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    data.traffic_1k_te_policy = False
    #check Tx Frame Rate
    ret = ixia_check_traffic(TRAFFIC_1K_TE_POLICY, key="Rx Frame Rate", value=100000, exact_match = False)
    if not ret:
        st.report_fail("Step17: Check traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    data.traffic_1k_te_policy = True
    ret = ixia_stop_traffic(TRAFFIC_1K_TE_POLICY)
    if not ret:
        st.report_fail("Step18: Stop traffic item {} rx frame failed".format(TRAFFIC_1K_TE_POLICY))
    data.traffic_1k_te_policy = False
    st.report_pass("test_case_passed")

'''
1. Dut1/Dut2 config 2k vrfs and 2k policy 
2. Each policy has 2 different priority cpaths
3. Each policy has a sbfd to detect
4. Shutdown/no shutdown interface on Dut1, sbfd flap
5. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_2k_policy_03():

    if data.dut2_load_2k_policy_config_done == False:
        st.log("esr_srte_policy_func_hooks enter test_srte_policy_2k_vrf_2k_policy_03")
        dut_load_config(dut2, "esr_te_dut2_2k_config")
        data.dut2_load_2k_policy_config_done = True
        data.dut2_load_1k_policy_config_done = False
        data.dut2_load_4k_policy_config_done = False

    if not retry_api(check_bgp_state, dut2, "2000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp state failed")

    ixia_disable_traffic(TRAFFIC_1K_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_2K_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step2: Start traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    st.wait(30)
    #check traffic cpath d, on interface Ethernet4
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 300, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step3: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)
    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step4: The cpath d: bfd-name d not down")

    #sbfd down, cpath change to c
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet3"], 300, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step5: Check dut interface counters failed")

    #no shutdown inteface ,sbfd up, cpath change to d
    cmd = "interface {}\n no shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step6: The cpath d: bfd-name a not up")

    #check traffic back to Ethernet4
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 300, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step7: Check dut interface counters failed")
    st.wait(10)
    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step8: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    #check Tx Frame Rate
    ret = ixia_check_traffic(TRAFFIC_2K_TE_POLICY, key="Rx Frame Rate", value=100000, exact_match = False)
    if not ret:
        st.report_fail("Step9: Check traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step10: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    st.report_pass("test_case_passed")

'''
1. Dut1/Dut2 config 2k vrfs and 2k color only 
2. Each policy has 2 different priority cpaths
3. Each policy has a sbfd to detect
4. Shutdown/no shutdown interface on Dut1, sbfd flap
5. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_2k_policy_color_only_04():

    if data.dut2_load_2k_policy_config_done == False:
        st.log("esr_srte_policy_func_hooks enter test_srte_policy_2k_vrf_2k_policy_03")
        dut_load_config(dut2, "esr_te_dut2_2k_config")
        data.dut2_load_2k_policy_config_done = True
        data.dut2_load_1k_policy_config_done = False
        data.dut2_load_4k_policy_config_done = False

    del_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "no neighbor 2000::179 activate"'
    st.config(dut1, del_neighbor)
    st.wait(5)

    add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 1000::179 activate"'
    st.config(dut1, add_neighbor)
    st.wait(30)

    if not retry_api(check_bgp_state, dut2, "2000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp state failed")

    ixia_disable_traffic(TRAFFIC_1K_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_2K_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step2: Start traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    #check traffic cpath d, on interface Ethernet4
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 300, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step3: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)
    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step4: The cpath d: bfd-name d not down")

    #sbfd down, cpath change to c
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet3"], 300, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step5: Check dut interface counters failed")

    #no shutdown inteface ,sbfd up, cpath change to d
    cmd = "interface {}\n no shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)

    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step6: The cpath d: bfd-name a not up")

    #check traffic back to Ethernet4
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet4"], 300, retry_count= 3, delay= 5)
    if not ret:
        st.report_fail("Step7: Check dut interface counters failed")

    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step8: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    #check Rx Frame Rate
    ret = ixia_check_traffic(TRAFFIC_2K_TE_POLICY, key="Rx Frame Rate", value=100000, exact_match = False)
    if not ret:
        st.report_fail("Step9: Check traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step10: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    st.report_pass("test_case_passed")

'''
1. Dut1/Dut2 config 2k vrfs and 4k policy 
2. Each policy has one cpath
3. Each policy has a sbfd to detect
4. Shutdown/no shutdown interface on Dut1, sbfd flap
5. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_4k_policy_05():

    if data.dut2_load_4k_policy_config_done == False:
        st.log("esr_srte_policy_func_hooks enter test_srte_policy_2k_vrf_4k_policy_05")
        dut_load_config(dut2, "esr_te_dut2_4k_config")
        data.dut2_load_4k_policy_config_done = True
        data.dut2_load_2k_policy_config_done = False
        data.dut2_load_1k_policy_config_done = False

    if not retry_api(check_bgp_state, dut2, "2011::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 2011::179 state failed")
    if not retry_api(check_bgp_state, dut2, "2022::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 2022::179 state failed")
    if not retry_api(check_bgp_state, dut2, "2033::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 2033::179 state failed")
    if not retry_api(check_bgp_state, dut2, "2044::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 2044::179 state failed")

    add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 1000::179 activate"'
    st.config(dut2, add_neighbor)
    add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 2000::179 activate"'
    st.config(dut2, add_neighbor)
    st.wait(30)
    if not retry_api(check_bgp_state, dut2, "1000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 100::179 state failed")
    if not retry_api(check_bgp_state, dut2, "2000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 2000::179 state failed")
    st.wait(30)

    ixia_disable_traffic(TRAFFIC_1K_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_2K_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step1: Start traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    #check traffic cpath d, on interface Ethernet4
    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step2: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)
    #check bfd state
    check_filed = {
        'status':'down',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step3: The cpath d: bfd-name d not down")
    #sbfd down, cpath change to c
    ret = retry_api(check_dut_intf_tx_traffic_counters, dut2, ["Ethernet3"], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step4: Check dut interface counters failed")

    #shutdown Ethernet4
    cmd = "interface {}\n no shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(10)
    #check bfd state
    check_filed = {
        'status':'up',
        'peer_type' : 'echo',
        'multiplier': '3'
    }
    key = "bfd-name d"

    if not retry_api(check_bfd_state, dut2, key, check_filed, retry_count= 10, delay= 10):
        st.report_fail("Step5: The cpath d: bfd-name d not up")

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step6: Check dut interface counters failed")

    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step7: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    #check Rx Frame Rate
    ret = ixia_check_traffic(TRAFFIC_2K_TE_POLICY, key="Rx Frame Rate", value=100000, exact_match = False)
    if not ret:
        st.report_fail("Step8: Check traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step9: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    st.report_pass("test_case_passed")

'''
1. Dut1/Dut2 config 2k vrfs and 4k color only 
2. Each policy has one cpath
3. Each policy has a sbfd to detect
4. bgp flap
5. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_4k_policy_falp_06():
    activate_bgp_neighbor = False
    if data.dut2_load_4k_policy_config_done == False:
        st.log("esr_srte_policy_func_hooks enter test_srte_policy_2k_vrf_4k_policy_falp_06")
        dut_load_config(dut2, "esr_te_dut2_4k_config")
        data.dut2_load_4k_policy_config_done = True
        data.dut2_load_2k_policy_config_done = False
        data.dut2_load_1k_policy_config_done = False
        activate_bgp_neighbor = True

    TOPOLOGY = "Topology 1"
    DEVICE_GROUP = "Device Group 1"
    ETHERNET = "Ethernet 1"
    IPV4_NAME = "IPv4 1"
    BGP_PEER_NAME = "BGP Peer 1"
    if activate_bgp_neighbor is True:
        if not retry_api(check_bgp_state, dut2, "2011::179", retry_count= 6, delay= 10):
            st.report_fail("Step0: Check bgp 2011::179 state failed")
        if not retry_api(check_bgp_state, dut2, "2022::179", retry_count= 6, delay= 10):
            st.report_fail("Step0: Check bgp 2022::179 state failed")
        if not retry_api(check_bgp_state, dut2, "2033::179", retry_count= 6, delay= 10):
            st.report_fail("Step0: Check bgp 2033::179 state failed")
        if not retry_api(check_bgp_state, dut2, "2044::179", retry_count= 6, delay= 10):
            st.report_fail("Step0: Check bgp 2044::179 state failed")

        add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 1000::179 activate"'
        st.config(dut2, add_neighbor)
        add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 2000::179 activate"'
        st.config(dut2, add_neighbor)
        st.wait(30)

    if not retry_api(check_bgp_state, dut2, "1000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 100::179 state failed")
    if not retry_api(check_bgp_state, dut2, "2000::179", retry_count= 6, delay= 10):
        st.report_fail("Step0: Check bgp 2000::179 state failed")
    st.wait(30)

    ixia_disable_traffic(TRAFFIC_1K_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_2K_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step1: Start traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = True
    #check traffic cpath d, on interface Ethernet4
    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step2: Check dut interface counters failed")

    show_hw_route_count(dut1)
    show_hw_route_count(dut2)

    st.log("start flap")
    ixia_config_bgp_flapping(TOPOLOGY, DEVICE_GROUP, ETHERNET, IPV4_NAME, BGP_PEER_NAME, True)
    st.wait(20)
    ixia_config_bgp_flapping(TOPOLOGY, DEVICE_GROUP, ETHERNET, IPV4_NAME, BGP_PEER_NAME, False)
    st.wait(60)
    show_hw_route_count(dut1)
    show_hw_route_count(dut2)

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step3: Check dut interface counters failed")

    ret = ixia_stop_traffic(TRAFFIC_2K_TE_POLICY)
    if not ret:
        st.report_fail("Step4: Stop traffic item {} rx frame failed".format(TRAFFIC_2K_TE_POLICY))
    data.traffic_2k_te_policy = False
    st.report_pass("test_case_passed")

'''
1. Dut1/Dut2 config 2k vrfs config ipv4 ipv6 route
2. Check traffic
'''
@pytest.mark.community
@pytest.mark.community_pass
def test_srte_policy_2k_vrf_ipv4_ipv6_07():

    if not retry_api(check_bgp_route_count, dut2, "2000::179", "200000", True,  retry_count= 10, delay= 30):
        st.report_fail("Step1: Chek route count failed")

    if not retry_api(check_srv6_te_policy_active, dut2, "4003",  retry_count= 10, delay= 30):
        st.report_fail("Step2: Chek te policy active count failed")
    '''
    ixia_disable_traffic(TRAFFIC_IPV4_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_IPV6_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_IPV6_TE_POLICY)
    if not ret:
        st.report_fail("Step3: Start traffic item {} rx frame failed".format(TRAFFIC_IPV6_TE_POLICY))

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 10, delay= 30)
    if not ret:
        st.report_fail("Step4: Check dut interface counters failed")

    cmd = "interface {}\n shutdown\n".format("Ethernet3")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(180)

    if not retry_api(check_srv6_te_policy_active, dut2, "2003",  retry_count= 10, delay= 30):
        st.report_fail("Step5: Chek te policy active count failed")

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet1', 'Ethernet2'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step6: Check dut interface counters failed")

    cmd = "interface {}\n no shutdown\n".format("Ethernet3")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    cmd = "interface {}\n no shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(180)

    if not retry_api(check_srv6_te_policy_active, dut2, "4003",  retry_count= 10, delay= 30):
        st.report_fail("Step7: Chek te policy active count failed")

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step8: Check dut interface counters failed")

    ret = ixia_stop_traffic(TRAFFIC_IPV6_TE_POLICY)
    if not ret:
        st.report_fail("Step9: Stop traffic item {} rx frame failed".format(TRAFFIC_IPV6_TE_POLICY))

    add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv6 vpn" -c "no neighbor 2000::179 activate"'
    st.config(dut2, add_neighbor)
    st.wait(30)
    add_neighbor = 'vtysh -c "configure terminal" -c "router bgp 100" -c "address-family ipv4 vpn" -c "neighbor 2000::179 activate"'
    st.config(dut2, add_neighbor)
    st.wait(30)

    if not retry_api(check_bgp_route_count, dut2, "2000::179", "200000",  retry_count= 10, delay= 30):
        st.report_fail("Step10: Chek route count failed")

    ixia_disable_traffic(TRAFFIC_IPV6_TE_POLICY)
    ixia_enable_traffic(TRAFFIC_IPV4_TE_POLICY)
    ret = ixia_start_traffic(TRAFFIC_IPV4_TE_POLICY)
    if not ret:
        st.report_fail("Step11: Start traffic item {} rx frame failed".format(TRAFFIC_IPV4_TE_POLICY))

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet3', 'Ethernet4'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step12: Check dut interface counters failed")

    cmd = "interface {}\n shutdown\n".format("Ethernet3")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    cmd = "interface {}\n shutdown\n".format("Ethernet4")
    st.config(dut2, cmd, type="alicli", skip_error_check = True)
    st.wait(180)
    if not retry_api(check_srv6_te_policy_active, dut2, "2003",  retry_count= 10, delay= 30):
        st.report_fail("Step13: Chek te policy active count failed")

    ret = retry_api(check_mult_dut_intf_tx_traffic_counters, dut2, ['Ethernet1', 'Ethernet2'], 300, retry_count= 5, delay= 10)
    if not ret:
        st.report_fail("Step14: Check dut interface counters failed")

    ret = ixia_stop_traffic(TRAFFIC_IPV4_TE_POLICY)
    if not ret:
        st.report_fail("Step15: Stop traffic item {} rx frame failed".format(TRAFFIC_IPV4_TE_POLICY))
    '''
    st.report_pass("test_case_passed")