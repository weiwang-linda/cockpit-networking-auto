import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from page_objects.page_networking_ipv6_check import CockpitNetworkingIpv6Page
from utils.caseid import add_case_id, check_case_id


class TestNetworkingIpv6Check(CockpitNetworkingIpv6Page):
    """
    :avocado: enable
    :avocado: tags=cockpit_IPv6
    """

    @check_case_id
    def tearDown(self):
        self.driver.quit()
        pass

    #1.RHEVM-24327 Chek the basic IPv6 network status
    @add_case_id("RHEVM-24327")
    def test_basic_ipv6_network_status(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.check_basic_ipv6_network_status()

    #2.RHEMV-24328 Configure one NIC IPv6 with automatic mode
    @add_case_id("RHEVM-24328")
    def test_config_one_nic_ipv6_auto_mode(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.check_config_one_nic_ipv6_auto_mode()

    #3.RHEVM-24332 Configure one NIC IPv6 with Manual mode
    @add_case_id("RHEVM-24332")
    def test_config_one_nic_ipv6_manual_mode(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.check_config_one_nic_ipv6_manual_mode()

    #4.RHEVM-24333 create IPv6 bond with automatic mode through cockpit
    @add_case_id("RHEVM-24333")
    def test_create_ipv6_bond_automatic_mode(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.check_create_ipv6_bond_automatic_mode()

    #5.RHEVM-24334 Create IPv6 bond with Manual mode throuth cockpit
    @add_case_id("RHEVM-24334")
    def test_create_ipv6_bond_manual_mode(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.check_create_ipv6_bond_manual_mode()

    #6.RHEVM-24335 Create IPv6 of vlan over one NIC with Automatic mode throuth cockpit
    @add_case_id("RHEVM-24335")
    def test_create_ipv6_vlan_over_one_nic_automatic(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.create_ipv6_vlan_over_one_nic_automatic()

    #7.RHEVM-24336 Create IPv6 of vlan over one NIC with Automatic(DHCP only) mode throuth cockpit
    @add_case_id("RHEVM-24336")
    def test_create_ipv6_vlan_over_one_nic_dhcp_only(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.create_ipv6_vlan_over_one_nic_dhcp_only()

    #8.RHEVM-24337 Create IPv6 of vlan over one NIC with Manual mode throuth cockpit
    @add_case_id("RHEVM-24337")
    def test_create_ipv6_vlan_over_one_nic_manual(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.create_ipv6_vlan_over_one_nic_manual()

    #9.RHEVM-24338 Create IPv6 of vlan over bond with Automatic mode throuth cockpit
    @add_case_id("RHEVM-24338")
    def test_create_ipv6_vlan_over_bond_automatic(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.create_ipv6_vlan_over_bond_automatic()

    #10.RHEVM-24339 Create IPv6 of vlan over bond with Automatic(DHCP only) mode throuth cockpit
    @add_case_id("RHEVM-24339")
    def test_create_ipv6_vlan_over_bond_dhcp_only(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.create_ipv6_vlan_over_bond_dhcp_only()

    #11.RHEVM-24340 Create IPv6 of vlan over bond with Manual mode throuth cockpit
    @add_case_id("RHEVM-24340")
    def test_create_ipv6_vlan_over_bond_manual(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.create_ipv6_vlan_over_bond_manual()

    #12.RHEVM-24341 Multiple NICs can be configured as IPv6 throuth cockpit
    @add_case_id("RHEVM-24341")
    def test_configure_multipul_nics_at_once(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.configure_multipul_nics_at_once()

    #13.RHEVM-24344 Delete bond through cockpit
    @add_case_id("RHEVM-24344")
    def test_delete_ipv6_bond(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.delete_ipv6_bond()

    #14.RHEVM-24343 Delete vlan through cockpit
    @add_case_id("RHEVM-24343")
    def test_delete_ipv6_vlan(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.delete_ipv6_vlan()

    #15.RHEVM-24345 Delete vlan over bond through cockpit
    @add_case_id("RHEVM-24345")
    def test_delete_ipv6_vlan_over_bond(self):
        """
        :avocado: tags=IPv6_tier1
        """
        self.delete_ipv6_vlan_over_bond()

    #16.RHEVM-24342 Check networking after add RHVH to RHEVM
    @add_case_id("RHEVM-24342")
    def test_check_network_after_add_rhvh_to_rhvm(self):
        """
        :avocado: tags=IPv6_tier
        """
        self.check_network_after_add_rhvh_to_rhvm()

    #17.RHEVM-24346 Setup IPv6 Link local mode
    @add_case_id("RHEVM-24346")
    def test_config_one_nic_ipv6_link_local_mode(self):
        """
        :avocado: tags=IPv6_tier2
        """
        self.check_config_one_nic_ipv6_link_local_mode()