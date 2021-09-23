import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_networking_check import CockpitNetworkingPage
from utils.caseid import add_case_id, check_case_id


class TestNetworkingCheck(CockpitNetworkingPage):
    """
    :avocado: enable
    :avocado: tags=cockpit_networking
    """

    # @check_case_id
    # def tearDown(self):
    #     pass

    # #1.RHEVM-23957 Check the basic network status
    # @add_case_id("RHEVM-23957")
    # def test_basic_network_status(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.check_basic_network_status()

    # #2.RHEMV-23958 Configure one NIC with dhcp mode
    # @add_case_id("RHEVM-23958")
    # def test_config_one_nic_dhcp_mode(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.check_config_one_nic_dhcp_mode()

    # #3.RHEVM-23959 Configure one NIC with Manual mode
    # @add_case_id("RHEVM-23959")
    # def test_config_one_nic_manual_mode(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.check_config_one_nic_manual_mode()

    # #4.RHEVM-23960 create bond(mode 0, active-backup) through cockpit
    # @add_case_id("RHEVM-23960")
    # def test_create_bond_dhcp_mode(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.check_create_bond_dhcp_mode()

    # #5.RHEVM-23968 Create bond(mode 0) through cockpit with static IP
    # @add_case_id("RHEVM-23968")
    # def test_create_bond_manual_mode(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.check_create_bond_manual_mode()

    # #6.RHEVM-23962 Create vlan(dhcp) through cockpit
    # @add_case_id("RHEVM-23962")
    # def test_create_vlan_over_one_nic_dhcp(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.create_vlan_over_one_nic_dhcp()

    # #7.RHEVM-23970 Create vlan through cockpit with static IP
    # @add_case_id("RHEVM-23970")
    # def test_create_vlan_over_one_nic_manual(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.create_vlan_over_one_nic_manual()

    # #8.RHEVM-23963 Create vlan+bond(dhcp) through cockpit
    # @add_case_id("RHEVM-23963")
    # def test_create_vlan_over_bond_automatic(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.create_vlan_over_bond_automatic()

    # #9.RHEVM-23969 Create bond+vlan through cockpit with static IP
    # @add_case_id("RHEVM-23969")
    # def test_create_vlan_over_bond_manual(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.create_vlan_over_bond_manual()

    # #10.RHEVM-23964 Multiple NICs can be configured through cockpit
    # @add_case_id("RHEVM-23964")
    # def test_configure_multipul_nics_at_once(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.configure_multipul_nics_at_once()

    # #11.RHEVM-23972 Delete bond through cockpit
    # @add_case_id("RHEVM-23972")
    # def test_delete_networking_bond(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.delete_networking_bond()

    # #12.RHEVM-23971 Delete vlan through cockpit
    # @add_case_id("RHEVM-23971")
    # def test_delete_networking_vlan(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.delete_networking_vlan()

    # #13.RHEVM-23973 Delete bond+vlan through cockpit
    # @add_case_id("RHEVM-23973")
    # def test_delete_networking_vlan_over_bond(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.delete_networking_vlan_over_bond()

    # #14.RHEVM-23965 Configure ifcfg script for network interface manually and persist it
    # @add_case_id("RHEVM-23965")
    # def test_config_ifcfg_script_for_network(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.config_ifcfg_script_for_network()

    # #15.RHEVM-23967 Check networking after add RHVH to RHEVM
    # @add_case_id("RHEVM-23967")
    # def test_check_network_after_add_rhvh_to_rhvm(self):
    #     """
    #     :avocado: tags=networking_tier1
    #     """
    #     self.check_network_after_add_rhvh_to_rhvm()

    # #16.RHEVM-23961 Create bridge through cockpit
    # @add_case_id("RHEVM-23961")
    # def test_check_create_bridge(self):
    #     """
    #     :avocado: tags=networking_tier2
    #     """
    #     self.check_create_bridge()

    # #17.RHEVM-23974 Delete bridge through cockpit
    # @add_case_id("RHEVM-23974")
    # def test_check_delete_bridge(self):
    #     """
    #     :avocado: tags=networking_tier2
    #     """
    #     self.check_delete_bridge()

    # #18.RHEVM-23975 Setup Link local mode successful
    # @add_case_id("RHEVM-23975")
    # def test_config_one_nic_link_local_mode(self):
    #     """
    #     :avocado: tags=networking_tier2
    #     """
    #     self.check_config_one_nic_link_local_mode()

    # #19.RHEVM-23976 Setup Shared mode successful
    # @add_case_id("RHEVM-23976")
    # def test_config_one_nic_shared_mode(self):
    #     """
    #     :avocado: tags=networking_tier2
    #     """
    #     self.check_config_one_nic_shared_mode()

    #20.RHEVM-25740 Setting firewall on/off
    #TODO:step4
    @add_case_id("RHEVM-25740")
    def test_config_firewall(self):
        """
        :avocado: tags=networking_tier1
        """
        self.check_config_firewall()

    #21.RHEVM-25741 Add/Delete service in firewall
    @add_case_id("RHEVM-25741")
    def test_add_del_svc_in_firewall(self):
        """
        :avocado: tags=networking_tier2
        """
        self.check_add_del_svc_in_firewall()
