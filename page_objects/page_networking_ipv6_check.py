import os
import simplejson
import yaml
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .seleniumlib import SeleniumTest
from rhvhauto_common_utils.rhv.base import BaseRhvAPI


progress_log = logging.getLogger("progress")

class CockpitNetworkingIpv6Page(SeleniumTest):
    """
    :avocado: disable
    """
    #Tips:
    #eno1 and eno2 represent two public NICs
    #eno3 and eno4 represent two internal NICs

    FABRIC_TIMEOUT = 300
    YUM_UPDATE_TIMEOUT = 1200
    YUM_INSTALL_TIMEOUT = 1200
    CHK_HOST_ON_RHVM_STAT_MAXCOUNT = 20
    CHK_HOST_ON_RHVM_STAT_INTERVAL = 60
    RHVM_DATA_MAP = {
        "4.0_rhvm_fqdn": "rhvm40-vlan50-2.lab.eng.pek2.redhat.com",
        "4.1_rhvm_fqdn": "vm-198-141.lab.eng.pek2.redhat.com",
        "4.2_rhvm_fqdn": "bootp-73-199-109.lab.eng.pek2.redhat.com",
        "4.3_rhvm_fqdn": "https://vm-198-110.lab.eng.pek2.redhat.com/ovirt-engine/api",
        "4.4_rhvm_fqdn": "https://vm-198-50.lab.eng.pek2.redhat.com/ovirt-engine/api",
        "4.4_rhvm_fqdn": "https://bootp-73-199-27.lab.eng.pek2.redhat.com/ovirt-engine/api",
    }

    RHVM_COMPUTE_MAP = {
        "dc_name": "networking-test",
        "cluster_name": "networking-test",
        "host_name": "networking-test",
    }

    ENTER_SYSTEM_MAXCOUNT = 10
    ENTER_SYSTEM_INTERVAL = 60
    ENTER_SYSTEM_TIMEOUT = 600

    SLEEP_TIME = 3
    WAIT_IP_READY = 30
    WAIT_IPV6_READY = 60
    #OVIRT_DASHBOARD_FRAME_NAME = "/ovirt-dashboard"
    OVIRT_DASHBOARD_FRAME_NAME = "/cockpit1:localhost/network"
    DASHBOARD_LINK = "a[href='#/dashboard']"

    #First menu named by IP address on the left
    HOST_LOCALHOST_MENU= "//a[@id='host-nav-link']"

    # System
    NETWORK_INFO_LINK = "tbody:nth-child(4) tr:nth-child(1) a"

    #Networking frame
    NETWORKING_FRAME = "cockpit1:localhost/network"
    #"Networking" menu on left side
    NETWORKING_MENU = "//a[@href='/network']"

    #"Reconnect" button after reboot
    RECONNECT_BUTTON = "//div[@class='blank-slate-pf-main-action']/button[@id='machine-reconnect']"

    #The "System" menu on left side
    SYSTEM_MENU = "//a[@href='/system']"
    SYSTEM_FRAME = "cockpit1:localhost/system"
    SYSTEM_VERSION = "//div[@id='system_information_os_text']"
    
    #The "Restart" button on "System" page
    SYSTEM_RESTART_BUTTON = "//button[text()='Reboot']"
    
    #The "1 Minute" drop-down list
    SYSTEM_RESTART_DELAY_1_MINUTE = "//button[@id='delay']"

    #The "No Delay" item on "Delay" drop-down list 
    # SYSTEM_RESTART_DELAY_NO_DELAY = "//div[@class='pf-c-select pf-m-expanded']//button[text()='No delay']"
    SYSTEM_RESTART_DELAY_NO_DELAY = "//div[@class='pf-c-select pf-m-expanded shutdown-select-delay']//button[text()='No delay']"  ###4.4.9

    #The "Restart" button on "Restart" page
    SYSTEM_RESTART_RESTART_BUTTON = "//button[@class='pf-c-button pf-m-danger']"

    #NICs enter link
    NETWORK_INFO_NICS = "//div//article[@id='networking-interfaces']/table/tbody"
    NETWORK_INFO_NICS_ENO1 = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno1']//button[contains(text(),'eno1')]"
    NETWORK_INFO_NICS_ENO2 = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno2']//button[contains(text(),'eno2')]"
    NETWORK_INFO_NICS_ENO3 = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno3']//button[contains(text(),'eno3')]"
    NETWORK_INFO_NICS_ENO4 = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno4']//button[contains(text(),'eno4')]"
    NETWORK_INFO_NICS_VLAN_OVER_ENO3 = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno3.50']//button[contains(text(),'eno3.50')]"
    NETWORK_INFO_NICS_VLAN_OVER_ENO4 = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno4.50']//button[contains(text(),'eno4.50')]"
    NETWORK_INFO_NICS_VLAN_OVER_BOND = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='test-bond0.50']//button[contains(text(),'test-bond0.50')]"

    #IP Address column after NICs
    NETWORK_INFO_NICS_ENO1_IP_ADDRESS = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno1']/td[@data-label='IP address']"
    NETWORK_INFO_NICS_ENO2_IP_ADDRESS = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno2']/td[@data-label='IP address']"
    NETWORK_INFO_NICS_ENO3_IP_ADDRESS = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno3']/td[@data-label='IP address']"
    NETWORK_INFO_NICS_BOND_IP_ADDRESS = "//div//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='test-bond0']//button[contains(text(),'test-bond0')]"
    NETWORK_INFO_NICS_VLAN_OVER_ENO3_IP_ADDRESS = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno3.50']//button[contains(text(),'eno3.50')]"
    NETWORK_INFO_NICS_VLAN_OVER_ENO4_IP_ADDRESS = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno4.50']//button[contains(text(),'eno4.50')]"
    NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='test-bond0.50']//button[contains(text(),'test-bond0.50')]"


    #Sending column link
    NETWORK_INFO_NICS_ENO1_SENDING = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno1']/td[@data-label='Sending']"
    NETWORK_INFO_NICS_ENO2_SENDING = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno2']/td[@data-label='Sending']"
    NETWORK_INFO_NICS_ENO3_SENDING = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno3']/td[@data-label='Sending']"
    NETWORK_INFO_NICS_ENO4_SENDING = "//article[@id='networking-interfaces']/table/tbody/tr[@data-interface='eno4']/td[@data-label='Sending']"


    #the ON/OFF button and Connect automatically check box
    CONNECT_AUTOMATICALLY_CHECK_BOX = "//dl[@id='network-interface-settings']//label[text()='Connect automatically']"
    NETWORK_NICS_ON = "//article[@class='pf-c-card network-interface-details']//span[@class='pf-c-switch__toggle']"
    NETWORK_NICS_OFF = "//article[@class='pf-c-card network-interface-details']//span[@class='pf-c-switch__toggle']"

    #The "Delete" button in NICs(bond) page
    BOND_VLAN_DELETE_BUTTON = "//button[@id='network-interface-delete']"

    #Status in Networking -> NICs/Bond/Vlan
    STATUS_LINK = "//dl[@id='network-interface-settings']//span[text()='Status']/../following-sibling::*//div"
    
    #IPv4 Settings link in NICs page
    IPV4_CONFIG_LINK = "//dl[@id='network-interface-settings']//span[text()='IPv4']/../following-sibling::*//button[contains(text(), 'edit')]"
    IPV4_MODE_NAME = "//dl[@id='network-interface-settings']//span[text()='IPv4']/../following-sibling::*//span[@class='network-interface-settings-text']"
    # IPV4_SETTING_DROP_DOWN_LIST = "//div[@id='network-ip-settings-body']//select[@class='ct-select col-left']"
    IPV4_SETTING_DROP_DOWN_LIST = "//div[@id='network-ip-settings-body']//select[@class='pf-c-form-control col-left']"  ###4.4.9
    IPV4_SETTING_DROP_DOWN_LIST_AUTOMATIC = "//div[@data-field='addresses']//option[contains(text(), 'Automatic (DHCP)')]"
    IPV4_SETTING_DROP_DOWN_LIST_MANUAL= "//div[@data-field='addresses']//option[contains(text(),'Manual')]"
    IPV4_SETTING_DROP_DOWN_LIST_DISABLED= "//div[@data-field='addresses']//option[contains(text(),'Disabled')]"
    IPV4_SETTING_DROP_DOWN_LIST_LINKLOCAL= "//div[@data-field='addresses']//option[contains(text(),'Link local')]"
    IPV4_SETTING_DROP_DOWN_LIST_SHARED= "//div[@data-field='addresses']//option[contains(text(),'Shared')]"
    # IPV4_SETTING_DELETE_MANUAL_IP_BUTTON = "//input[@placeholder='Gateway']/../following-sibling::*/button[@class='pf-c-button pf-m-secondary btn-sm']"
    IPV4_SETTING_DELETE_MANUAL_IP_BUTTON = "//input[@placeholder='Gateway']/../following-sibling::*/button[@class='pf-c-button pf-m-secondary pf-m-small']"  ### 4.4.9

    #IPv6 Settings link in NICs page
    IPV6_CONFIG_LINK = "//dl[@id='network-interface-settings']//span[text()='IPv6']/../following-sibling::*//button[contains(text(), 'edit')]"
    IPV6_MODE_NAME = "//dl[@id='network-interface-settings']//span[text()='IPv6']/../following-sibling::*//span[@class='network-interface-settings-text']"
    # IPV6_SETTING_DROP_DOWN_LIST = "//div[@id='network-ip-settings-body']//select[@class='ct-select col-left']"
    IPV6_SETTING_DROP_DOWN_LIST = "//div[@id='network-ip-settings-body']//select[@class='pf-c-form-control col-left']"  ###4.4.9
    IPV6_SETTING_DROP_DOWN_LIST_MANUAL = "//div[@data-field='addresses']//option[contains(text(),'Manual')]"
    IPV6_SETTING_DROP_DOWN_LIST_AUTOMATIC = "//div[@data-field='addresses']//option[contains(text(),'Automatic')]"
    IPV6_SETTING_DROP_DOWN_LIST_DHCP_ONLY = "//div[@data-field='addresses']//option[contains(text(),'Automatic (DHCP only)')]"
    IPV6_SETTING_DROP_DOWN_LIST_IGNORE = "//div[@data-field='addresses']//option[contains(text(),'Ignore')]"
    IPV6_SETTING_DROP_DOWN_LIST_LINKLOCAL = "//div[@data-field='addresses']//option[contains(text(),'Link local')]"
    # IPV6_SETTING_DELETE_MANUAL_IP_BUTTON = "//input[@placeholder='Gateway']/../following-sibling::*/button[@class='pf-c-button pf-m-secondary btn-sm']"
    IPV6_SETTING_DELETE_MANUAL_IP_BUTTON = "//input[@placeholder='Gateway']/../following-sibling::*/button[@class='pf-c-button pf-m-secondary pf-m-small']"  ### 4.4.9

    #Addresses text input box of manual mode
    INPUT = "//div[@id='network-ip-settings-body']/div/div/table/tr/td/input"
    INPUT_PREFIX = "//div[@id='network-ip-settings-body']/div/div/table/tr/td[2]/input"

    #Apply button of IPv6 Settings page
    IPV6_SETTING_APPLY_BUTTON = "//button[@id='network-ip-settings-apply']"

    #The "Networking" button in left side
    NETWORKING_MENU_LEFT_SIDE = "//a[@href='/network']"

    #The "Networking Logs" table in "Networking" page
    NETWORKING_LOGS = "//div[contains(text(),'Network logs')]"

    #The "Add Bond" button in "Networking" page
    ADD_BOND_BUTTON = "//button[@id='networking-add-bond']"

    #Elements in Bond Settings page
    BOND_SETTING_NAME = "//div[@id='network-bond-settings-dialog']//input[@id='network-bond-settings-interface-name-input']"
    BOND_SETTING_MEMBERS_CHECKBOX_ENO1 = "//div[@id='network-bond-settings-dialog']//ul[@class='list-group dialog-list-ct']//label/span[contains(text(),'eno1')]"
    BOND_SETTING_MEMBERS_CHECKBOX_ENO2 = "//div[@id='network-bond-settings-dialog']//ul[@class='list-group dialog-list-ct']//label/span[contains(text(),'eno2')]"
    BOND_SETTING_MEMBERS_CHECKBOX_ENO3 = "//div[@id='network-bond-settings-dialog']//ul[@class='list-group dialog-list-ct']//label/span[contains(text(),'eno3')]"
    BOND_SETTING_MEMBERS_CHECKBOX_ENO4 = "//div[@id='network-bond-settings-dialog']//ul[@class='list-group dialog-list-ct']//label/span[contains(text(),'eno4')]"
    BOND_SETTING_MAC_LIST = "//div[@id='network-bond-settings-dialog']//button[@class='btn btn-default dropdown-toggle']"
    BOND_SETTING_MAC_ENO1 = "//ul[@id='network-bond-settings-mac-menu']//a[contains(text(),'eno1')]"
    BOND_SETTING_MAC_ENO3 = "//ul[@id='network-bond-settings-mac-menu']//a[contains(text(),'eno3')]"
    # BOND_SETTING_PRIMARY_LIST = "//div[@id='network-bond-settings-dialog']//select[@class='ct-select form-control']"
    BOND_SETTING_PRIMARY_LIST = "//div[@id='network-bond-settings-dialog']//select[@class='pf-c-form-control form-control']"  ### 4.4.9
    # BOND_SETTING_PRIMARY_ENO1 = "//div[@id='network-bond-settings-dialog']//select[@class='ct-select form-control']/option[contains(text(),'eno1')]"
    # BOND_SETTING_PRIMARY_ENO3 = "//div[@id='network-bond-settings-dialog']//select[@class='ct-select form-control']/option[contains(text(),'eno3')]"
    BOND_SETTING_PRIMARY_ENO1 = "//div[@id='network-bond-settings-dialog']//select[@class='pf-c-form-control form-control']/option[contains(text(),'eno1')]"  ### 4.4.9
    BOND_SETTING_PRIMARY_ENO3 = "//div[@id='network-bond-settings-dialog']//select[@class='pf-c-form-control form-control']/option[contains(text(),'eno3')]"  ### 4.4.9
    BOND_SETTING_APPLY = "//div[@id='network-bond-settings-dialog']//button[@id='network-bond-settings-apply']"

    #bond mode in Bond page
    BOND_MODE_UNDER_BOND_NAME = "//dl[@id='network-interface-settings']//span[text()='Bond']/../following-sibling::*//span[@class='network-interface-settings-text']"
    
    #workaround-bug1817948-begin
    BOND_SETTING_MODE = "//div[@id='network-bond-settings-dialog']//select[@id='network-bond-settings-mode-select']"
    BOND_SETTING_MODE_XOR = "//div[@id='network-bond-settings-dialog']//select[@id='network-bond-settings-mode-select']/option[contains(text(),'XOR')]"
    BOND_SETTING_MODE_ACTIVE_BACKUP = "//div[@id='network-bond-settings-dialog']//select[@id='network-bond-settings-mode-select']/option[contains(text(),'Active backup')]"
    #workaround-bug1817948-end

    #The "Add VLAN" button in "Networking" page
    ADD_VLAN_BUTTON = "//button[@id='networking-add-vlan']"

    #Elements in "VLAN Settings" page
    VLAN_SETTING_PARENT_LIST = "//div[@id='network-vlan-settings-dialog']//select[@id='network-vlan-settings-parent-select']"
    VLAN_SETTING_PARENT_ENO3 = "//div[@id='network-vlan-settings-dialog']//option[contains(text(),'eno3')]"
    VLAN_SETTING_PARENT_ENO4 = "//div[@id='network-vlan-settings-dialog']//option[contains(text(),'eno4')]"
    VLAN_SETTING_PARENT_BOND = "//div[@id='network-vlan-settings-dialog']//option[contains(text(),'test-bond0')]"
    VLAN_SETTING_VLAN_ID = "//div[@id='network-vlan-settings-dialog']//input[@id='network-vlan-settings-vlan-id-input']"
    VLAN_SETTING_APPLY_BUTTON = "//div[@id='network-vlan-settings-dialog']//button[@id='network-vlan-settings-apply']"


    def open_page(self):
        b = self.get_data('networking_ipv6_config.yml')
        self.config_dict = yaml.load(open(b), Loader=yaml.FullLoader)

        self.driver.switch_to.default_content()
        # self.click(self.HOST_LOCALHOST_MENU)
        time.sleep(self.SLEEP_TIME)

        #click the "Networking" menu on left side
        self.click(self.NETWORKING_MENU)

        #back to the root html
        self.driver.switch_to.default_content()
        time.sleep(self.SLEEP_TIME)

        #switch to the networking frame
        self.switch_to_frame(self.NETWORKING_FRAME)

        #add ip route
        cmd = "ip route"
        ret_cmd = self.host.execute(cmd, timeout=self.ENTER_SYSTEM_TIMEOUT)
        progress_log.info("The ip route in host is: '{}'.".format(ret_cmd[1]))
        if not ret_cmd[0]:
            self.fail("Get route failed.")
            return False
        if "10.0.0.0/8 via" not in ret_cmd[1]:
            progress_log.info("Adding ip route 10.0.0.0/8 ...")
            self._add_10_route()

    
    #1.RHEVM-24327 Chek the basic IPv6 network status
    def check_basic_ipv6_network_status(self):
        #nics_name = ["eno1","eno2","eno3","eno4"]
        #ifcfg_files_name = ["ifcfg-eno1","ifcfg-eno2","ifcfg-eno3","ifcfg-eno4"]
        nics_name = [
            self.config_dict['NICs_eno1'], self.config_dict['NICs_eno2'],
            self.config_dict['NICs_eno3'], self.config_dict['NICs_eno4']]

        ifcfg_files_name = [
            self.config_dict['ifcfg_file_eno1'], self.config_dict['ifcfg_file_eno2'],
            self.config_dict['ifcfg_file_eno3'], self.config_dict['ifcfg_file_eno4']]

        #check all NICs via cockpit
        nics_name_cockpit = []
        trs = self.driver.find_element_by_xpath(self.NETWORK_INFO_NICS)
        ths = trs.find_elements_by_tag_name('th')
        for th in ths:
            nics_name_cockpit.append(th.text)

        for nic_name in nics_name:
            if nic_name not in nics_name_cockpit:
                self.fail("The NIC '{}' is not in cockpit.".format(nic_name))
                return False

        #When installing RHVH, open eno1, close eno2, eno3, and eno4. 
        #After the installation is complete, check the status of the NICs.
        #get NICs's status(inactive or not)
        eno1_ip_addresses = self.get_text(self.NETWORK_INFO_NICS_ENO1_IP_ADDRESS)
        if eno1_ip_addresses == "":
            self.fail("The NIC '{}' is not on.".format("eno1"))
            return False

        if self._check_if_nics_are_off(self.config_dict['NICs_eno2'], self.NETWORK_INFO_NICS_ENO2_SENDING)\
            or self._check_if_nics_are_off(self.config_dict['NICs_eno3'], self.NETWORK_INFO_NICS_ENO3_SENDING)\
                or self._check_if_nics_are_off(self.config_dict['NICs_eno4'], self.NETWORK_INFO_NICS_ENO4_SENDING):
            self.fail("After clean installing, closed NICs are not turned off.")
            return False

        #check NICs via RHVH shell
        ret = self.host.execute(self.config_dict['check_ips'], timeout=self.ENTER_SYSTEM_TIMEOUT)
        for nic_name in nics_name:
            if nic_name not in ret[1]:
                self.fail("The NIC '{}' is not in RHVH shell.".format(nic_name))
                return False

        #check ifcfg-$NIC files via RHVH shell
        self._check_ifcfg_files_via_shell(ifcfg_files_name)
        
        #check logs
        log_info_cockpit = []
        divs = self.driver.find_element_by_xpath(self.NETWORKING_LOGS)
        spans = divs.find_elements_by_tag_name('span')
        for span in spans:
            log_info_cockpit.append(span.text)
        if "<info>" in log_info_cockpit:
            return True

        #This function should be called before running all the other test cases
        #After installation, if the NIC's "Connection automacically" check-box is not selected, select it
        #self._click_checkbox_connection_automatically(self.NETWORK_INFO_NICS_ENO2, self.NETWORK_INFO_NICS_ENO2_SENDING)
        self._click_checkbox_connection_automatically(self.NETWORK_INFO_NICS_ENO3, self.NETWORK_INFO_NICS_ENO3_SENDING)
        self._click_checkbox_connection_automatically(self.NETWORK_INFO_NICS_ENO4, self.NETWORK_INFO_NICS_ENO4_SENDING)

    
    #2.RHEMV-24328 Configure one NIC IPv6 with automatic mode
    def check_config_one_nic_ipv6_auto_mode(self):
        
        #check ip via rhvh shell
        ipv6_text = self._get_ip_via_rhvh_shell("eno1", "IPv6")
        if ipv6_text == '':
            self.fail("Check IPv6 ip via rhvh shell fail.")
            return False

        #click eno1
        self.click(self.NETWORK_INFO_NICS_ENO1)
        time.sleep(self.SLEEP_TIME)

        #check IPv6 mode in the NIC
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_ENO1,
            Ipv6_mode_name=self.config_dict['IPv6_mode_auto'])


    #3.RHEVM-24332 Configure one NIC IPv6 with Manual mode
    def check_config_one_nic_ipv6_manual_mode(self):
        #click eno3
        eno3_status = self.get_text(self.NETWORK_INFO_NICS_ENO3_SENDING)
        self.click(self.NETWORK_INFO_NICS_ENO3)
        time.sleep(self.SLEEP_TIME)

        if eno3_status == "Inactive":
            #turn on the NIC
            self.click(self.NETWORK_NICS_ON)
            time.sleep(self.SLEEP_TIME)

        #config IPv6 to "Manual" mode
        self._ipv6_settings_config_mode(
            self.config_dict['IPv6_mode_manual'],
            self.IPV6_SETTING_DROP_DOWN_LIST_MANUAL)

        #check IPv6 mode in the NIC
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_ENO3,
            Ipv6_mode_name=self.config_dict['IPv6_mode_manual'])

        #after reboot, check ipv6 ip via shell 
        time.sleep(self.WAIT_IPV6_READY)
        ipv6_text = self._get_ip_via_rhvh_shell("eno3", "IPv6")
        #progress_log.info("************************ipv6_text='{}'.".format(ipv6_text))
        if not (ipv6_text == self.config_dict['ipv6_ip_in_shell']):
            self.fail("Manual mode: check IPv6 ip via rhvh shell fail.")
            return False

        #clean up the test environment--delete manual mode of NICs
        self._clean_environment_delete_manual_ip(self.NETWORK_INFO_NICS_ENO3, self.IPV6_CONFIG_LINK)
        time.sleep(self.SLEEP_TIME)

        return


    #4.RHEVM-24333 create IPv6 bond with automatic mode through cockpit
    def check_create_ipv6_bond_automatic_mode(self):

        #create bond and configure IPv4 and IPv6 to "Automatic" mode
        self._create_bond_and_setting_mode(
            self.config_dict['IPv4_mode_auto'],self.IPV4_SETTING_DROP_DOWN_LIST_AUTOMATIC, 
            self.config_dict['IPv6_mode_auto'],self.IPV6_SETTING_DROP_DOWN_LIST_AUTOMATIC)

        self._check_nics_status_after_setting()

        #check IPv4 and IPv6 mode in the bond
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_BOND_IP_ADDRESS,
            self.config_dict['IPv4_mode_auto'], self.config_dict['IPv6_mode_auto'])

        #check bond mode after reboot
        time.sleep(self.SLEEP_TIME)
        bond_mode_name = self.get_text(self.BOND_MODE_UNDER_BOND_NAME)
        if not (bond_mode_name == "Active backup"):
            self.fail("Bond mode error: Bond mode is not Active Backup after host reboot.")
            return False

        #Clean up the test environment-delete bond
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return


    #5.RHEVM-24334 Create IPv6 bond with Manual mode throuth cockpit
    def check_create_ipv6_bond_manual_mode(self):
        
        #create bond and set IPv4 and IPv6 to Manual mode
        self._create_bond_and_setting_mode(
            self.config_dict['IPv4_mode_manual'], self.IPV4_SETTING_DROP_DOWN_LIST_MANUAL, 
            self.config_dict['IPv6_mode_manual'],self.IPV6_SETTING_DROP_DOWN_LIST_MANUAL)

        #check IPv4 and IPv6 mode in the bond
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_BOND_IP_ADDRESS,
            self.config_dict['IPv4_mode_manual'], self.config_dict['IPv6_mode_manual'])

        #after reboot, check ipv4 and ipv6 ip via shell
        ipv4_text = self._get_ip_via_rhvh_shell("test-bond0", "IPv4")
        if not (ipv4_text == self.config_dict['ipv4_ip_in_shell']):
            self.fail("Manual mode: check IPv4 ip via rhvh shell fail.")
            return False

        ipv6_text = self._get_ip_via_rhvh_shell("test-bond0", "IPv6")
        if not (ipv6_text == self.config_dict['ipv6_ip_in_shell']) :
            self.fail("Manual mode: check IPv6 ip via rhvh shell fail.")
            return False
        
        #Clean up the test environment-delete bond
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return


    #6.RHEVM-24335 Create IPv6 of vlan over one NIC with Automatic mode throuth cockpit
    def create_ipv6_vlan_over_one_nic_automatic(self):
        #create VLAN and configure IPv4 and IPv6 to "Automatic" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_ENO3, self.NETWORK_INFO_NICS_VLAN_OVER_ENO3_IP_ADDRESS, 
            self.config_dict['IPv4_mode_auto'], self.IPV4_SETTING_DROP_DOWN_LIST_AUTOMATIC, 
            self.config_dict['IPv6_mode_auto'], self.IPV6_SETTING_DROP_DOWN_LIST_AUTOMATIC)

        #check IPv4 and IPv6 mode in the VLAN
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_VLAN_OVER_ENO3,
            self.config_dict['IPv4_mode_auto'], self.config_dict['IPv6_mode_auto'])
        
        self._check_nics_status_after_setting()

        #Clean up the test environment-delete VLAN
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return


    #7.RHEVM-24336 Create IPv6 of vlan over one NIC with Automatic(DHCP only) mode throuth cockpit
    def create_ipv6_vlan_over_one_nic_dhcp_only(self):

        #create VLAN and configure IPv6 to "Automatic(DHCP only)" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_ENO4, self.NETWORK_INFO_NICS_VLAN_OVER_ENO4_IP_ADDRESS, 
            ipv6_mode_name=self.config_dict['IPv6_mode_dhcp'], ipv6_mode_link=self.IPV6_SETTING_DROP_DOWN_LIST_DHCP_ONLY)

        #check IPv6 mode in the VLAN
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_VLAN_OVER_ENO4_IP_ADDRESS,
            Ipv6_mode_name=self.config_dict['IPv6_mode_dhcp'])

        self._check_nics_status_after_setting()
        
        #Clean up the test environment-delete VLAN
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return


    #8.RHEVM-24337 Create IPv6 of vlan over one NIC with Manual mode throuth cockpit
    def create_ipv6_vlan_over_one_nic_manual(self):
        #create VLAN and configure IPv6 to "Manual" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_ENO4, self.NETWORK_INFO_NICS_VLAN_OVER_ENO4_IP_ADDRESS, 
            ipv6_mode_name=self.config_dict['IPv6_mode_manual'], ipv6_mode_link=self.IPV6_SETTING_DROP_DOWN_LIST_MANUAL)

        #check IPv6 mode in the VLAN
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_VLAN_OVER_ENO4_IP_ADDRESS,
            Ipv6_mode_name=self.config_dict['IPv6_mode_manual'])

        #after reboot, check ipv6 ip via shell
        ipv6_text = self._get_ip_via_rhvh_shell("eno4.50", "IPv6")
        if not (ipv6_text == self.config_dict['ipv6_ip_in_shell']) :
            self.fail("Manual mode: check vlan over eno4 IPv6 ip via rhvh shell fail.")
            return False

        #Clean up the test environment-delete VLAN
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return


    #9.RHEVM-24338 Create IPv6 of vlan over bond with Automatic mode throuth cockpit
    def create_ipv6_vlan_over_bond_automatic(self):

        #create bond and set IPv4 as "Disabled", set IPv6 as "Ignore"
        self._create_bond_and_setting_mode(
            self.config_dict['IPv4_mode_disabled'], self.IPV4_SETTING_DROP_DOWN_LIST_DISABLED, 
            self.config_dict['Ipv6_mode_ignore'], self.IPV6_SETTING_DROP_DOWN_LIST_IGNORE)

        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        #Return to default html frame
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        #create VLAN over bond and configure IPv6 to "Automatic" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_BOND, self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS, 
            ipv6_mode_name=self.config_dict['IPv6_mode_auto'], ipv6_mode_link=self.IPV6_SETTING_DROP_DOWN_LIST_AUTOMATIC)

        #check IPv6 mode in the VLAN
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS, Ipv6_mode_name=self.config_dict['IPv6_mode_auto'])

        self._check_nics_status_after_setting()
        
        #Clean up the test environment - delete vlan over bond, delete bond
        self._clean_up_test_environment_vlan_over_bond()
        time.sleep(self.SLEEP_TIME)

        return


    #10.RHEVM-24339 Create IPv6 of vlan over bond with Automatic(DHCP only) mode throuth cockpit
    def create_ipv6_vlan_over_bond_dhcp_only(self):
        #create bond and set IPv4 as "Disabled", set IPv6 as "Ignore"
        self._create_bond_and_setting_mode(
            self.config_dict['IPv4_mode_disabled'], self.IPV4_SETTING_DROP_DOWN_LIST_DISABLED, 
            self.config_dict['Ipv6_mode_ignore'], self.IPV6_SETTING_DROP_DOWN_LIST_IGNORE)

        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        #create VLAN over bond and configure IPv6 to "Automatic (DHCP only)" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_BOND, self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS,
            ipv6_mode_name=self.config_dict['IPv6_mode_dhcp'], ipv6_mode_link=self.IPV6_SETTING_DROP_DOWN_LIST_DHCP_ONLY)

        #check IPv6 mode in the VLAN
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS, Ipv6_mode_name=self.config_dict['IPv6_mode_dhcp'])

        self._check_nics_status_after_setting()

        #Clean up the test environment - delete vlan over bond, delete bond
        self._clean_up_test_environment_vlan_over_bond()
        time.sleep(self.SLEEP_TIME)

        return


    #11.RHEVM-24340 Create IPv6 of vlan over bond with Manual mode throuth cockpit
    def create_ipv6_vlan_over_bond_manual(self):
        #create bond and set IPv4 as "Disabled", set IPv6 as "Ignore"
        self._create_bond_and_setting_mode(
            self.config_dict['IPv4_mode_disabled'], self.IPV4_SETTING_DROP_DOWN_LIST_DISABLED,
            self.config_dict['Ipv6_mode_ignore'], self.IPV6_SETTING_DROP_DOWN_LIST_IGNORE)

        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        #create VLAN over bond and configure IPv6 to "Manual" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_BOND, self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS, 
            ipv6_mode_name=self.config_dict['IPv6_mode_manual'], ipv6_mode_link=self.IPV6_SETTING_DROP_DOWN_LIST_MANUAL)

        #check IPv6 mode in the VLAN
        self._check_nic_mode_before_and_after_reboot(
            self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS, Ipv6_mode_name=self.config_dict['IPv6_mode_manual'])

        #after reboot, check ipv4 and ipv6 ip via shell
        ipv6_text = self._get_ip_via_rhvh_shell("test-bond0.50", "IPv6")
        if not (ipv6_text == self.config_dict['ipv6_ip_in_shell']):
            self.fail("Manual mode: check vlan over bond IPv6 ip via rhvh shell fail.")
            return False

        #Clean up the test environment - delete vlan over bond, delete bond
        self._clean_up_test_environment_vlan_over_bond()
        time.sleep(self.SLEEP_TIME)

        return


    #12.RHEVM-24341 Multiple NICs can be configured as IPv6 throuth cockpit
    def configure_multipul_nics_at_once(self):
        #ifcfg_files_name = ["ifcfg-eno1","ifcfg-eno2","ifcfg-eno3","ifcfg-eno4"]
        ifcfg_files_name = [
            self.config_dict['ifcfg_file_eno1'], self.config_dict['ifcfg_file_eno2'],
            self.config_dict['ifcfg_file_eno3'], self.config_dict['ifcfg_file_eno4']]

        #open eno2
        self._click_checkbox_connection_automatically(self.NETWORK_INFO_NICS_ENO2, self.NETWORK_INFO_NICS_ENO2_SENDING)
        
        #configure eno2 as IPv4 Manual and IPv6 Manual
        self._configure_one_nic_ipv4_ipv6_with_specified_mode(
            self.NETWORK_INFO_NICS_ENO2, self.NETWORK_INFO_NICS_ENO2_SENDING, 
            self.config_dict['IPv4_mode_link'], self.IPV4_SETTING_DROP_DOWN_LIST_LINKLOCAL, 
            self.config_dict['IPv6_mode_link'], self.IPV6_SETTING_DROP_DOWN_LIST_LINKLOCAL)

        #configure eno3 as IPv4 Aumatic and IPv6 Automatic DHCP only
        self._configure_one_nic_ipv4_ipv6_with_specified_mode(
            self.NETWORK_INFO_NICS_ENO3, self.NETWORK_INFO_NICS_ENO3_SENDING, 
            self.config_dict['IPv4_mode_shared'], self.IPV4_SETTING_DROP_DOWN_LIST_SHARED, 
            self.config_dict['IPv6_mode_dhcp'], self.IPV6_SETTING_DROP_DOWN_LIST_DHCP_ONLY)

        #configure eno4 as IPv4 Automatic and IPv6 Automatic
        self._configure_one_nic_ipv4_ipv6_with_specified_mode(
            self.NETWORK_INFO_NICS_ENO4, self.NETWORK_INFO_NICS_ENO4_SENDING, 
            self.config_dict['IPv4_mode_disabled'], self.IPV4_SETTING_DROP_DOWN_LIST_DISABLED, 
            self.config_dict['Ipv6_mode_ignore'], self.IPV6_SETTING_DROP_DOWN_LIST_IGNORE)

        #reboot system and login cockpit again
        self._reboot_and_login_in_again()

        #check if NICs configuration are correct
        self._check_nic_mode_settings_after_reboot(
            self.NETWORK_INFO_NICS_ENO2, 
            self.config_dict['IPv4_mode_link'], self.config_dict['IPv6_mode_link'])

        self._check_nic_mode_settings_after_reboot(
            self.NETWORK_INFO_NICS_ENO3, 
            self.config_dict['IPv4_mode_shared'], self.config_dict['IPv6_mode_dhcp'])

        self._check_nic_mode_settings_after_reboot(
            self.NETWORK_INFO_NICS_ENO4, 
            self.config_dict['IPv4_mode_disabled'], self.config_dict['Ipv6_mode_ignore'])

        #after reboot, check ipv6 ip via shell 
        # ipv6_text = self._get_ip_via_rhvh_shell("eno3", "IPv6")
        # if not (ipv6_text == self.config_dict['ipv6_ip_in_shell']):
        #     self.fail("Manual mode: check IPv6 ip via rhvh shell fail.")
        #     return False

        #check ifcfg-$NIC files via RHVH shell
        self._check_ifcfg_files_via_shell(ifcfg_files_name)

        #close eno2
        self._click_checkbox_connection_automatically(self.NETWORK_INFO_NICS_ENO2, self.NETWORK_INFO_NICS_ENO2_SENDING,turn_on=False)
        time.sleep(self.SLEEP_TIME)

        return


    #13.RHEVM-24344 Delete bond through cockpit
    def delete_ipv6_bond(self):

        #create bond and configure IPv4 and IPv6 to "Automatic(DHCP)" mode
        self._create_bond_and_setting_mode()

        #delete bond
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #after deleting bond, check if slave NICs are on
        time.sleep(self.WAIT_IP_READY)
        if not self._check_if_nics_are_off(self.config_dict['NICs_eno3'], self.NETWORK_INFO_NICS_ENO3_SENDING)\
            or not self._check_if_nics_are_off(self.config_dict['NICs_eno4'], self.NETWORK_INFO_NICS_ENO4_SENDING):
            self.fail("After deleting bond, slave NICs are not up.")
            return False


    #14.RHEVM-24343 Delete vlan through cockpit
    def delete_ipv6_vlan(self):
        
        #create VLAN on eno3 and IPv4 to "Automatic(DHCP)" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_ENO3, self.NETWORK_INFO_NICS_VLAN_OVER_ENO3_IP_ADDRESS)

        #delete vlan
        self._clean_environment_delete_bond_vlan(
            self.NETWORK_INFO_NICS_VLAN_OVER_ENO3_IP_ADDRESS)
        time.sleep(self.SLEEP_TIME)

        return


    #15.RHEVM-24345 Delete vlan over bond through cockpit
    def delete_ipv6_vlan_over_bond(self):
        
        #create bond, set IPv4 and IPv6 as default
        self._create_bond_and_setting_mode()

        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        #Return to default html frame
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        #create VLAN over bond and IPv4 to "Automatic(DHCP)" mode
        self._create_vlan_and_setting_mode(
            self.VLAN_SETTING_PARENT_BOND, self.NETWORK_INFO_NICS_VLAN_OVER_BOND_IP_ADDRESS)

        #delete vlan over bond, then delete bond
        self._clean_up_test_environment_vlan_over_bond()
        time.sleep(self.SLEEP_TIME)

        return

        
    #16.RHEVM-24342 Check networking after add RHVH to RHEVM
    def check_network_after_add_rhvh_to_rhvm(self):
        nics_name = [
            self.config_dict['NICs_eno1'], self.config_dict['NICs_eno2'],
            self.config_dict['NICs_eno3'], self.config_dict['NICs_eno4'],
            self.config_dict['NICs_ovirt']
        ]

        #add host to RHVH
        if not self._add_host_to_rhvm():
            self.fail("Add host to RHVH failed.")
            return False

        #check host status in RHVM
        if not self._check_host_status_on_rhvm():
            self.fail("Host is not up in RHVM.")
            return False

        #check NICs via RHVH shell
        ret = self.host.execute(self.config_dict['check_ips'], timeout=self.ENTER_SYSTEM_TIMEOUT)
        for nic_name in nics_name:
            if nic_name not in ret[1]:
                self.fail("The NIC '{}' is not in RHVH shell.".format(nic_name))
                return False

        #clean test environment - delete data center, cluster and host on RHVM
        self._del_host_on_rhvm()
        time.sleep(self.SLEEP_TIME)

        return


    #17.RHEVM-24346 Setup IPv6 Link local mode
    def check_config_one_nic_ipv6_link_local_mode(self):
        #configure eno4 as IPV6 Link local mode
        self._configure_one_nic_ipv4_ipv6_with_specified_mode(
            self.NETWORK_INFO_NICS_ENO4,
            self.NETWORK_INFO_NICS_ENO4_SENDING, 
            ipv6_mode_name=self.config_dict['IPv6_mode_link'], 
            ipv6_mode_link=self.IPV6_SETTING_DROP_DOWN_LIST_LINKLOCAL)
        
        #reboot system and login cockpit again
        self._reboot_and_login_in_again()

        #check if NICs configuration are correct
        self._check_nic_mode_settings_after_reboot(
            self.NETWORK_INFO_NICS_ENO4, ipv6_mode_name=self.config_dict['IPv6_mode_link'])
        
        return


    ''' Internal function '''
    def _check_nics_status_after_setting(self):
        #waiting vlan to get ip
        time.sleep(self.WAIT_IPV6_READY)

        #check NICs status
        nics_status = self.get_text(self.STATUS_LINK)
        time.sleep(self.SLEEP_TIME)
        if nics_status == "Inactive":
            self.log.warning("Created Bond/Vlan/Vlan over Bond is Inactive.")
        
        return
    
    #check if NICs status is off
    def _check_if_nics_are_off(self, nic_name, ip_link):
        nic_status = self.get_text(ip_link)
        if nic_status == "Inactive":
            progress_log.info("The NIC '{}' is off.".format(nic_name))
            return False
        else:
            progress_log.info("The NIC '{}' is up.".format(nic_name))
            return True

    #After installation, if the NIC's "Connection automacically" check-box is not selected, select it
    def _click_checkbox_connection_automatically(self, nic_link, nic_sending_link, turn_on=True):
        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        if turn_on:
            #if the NICs is off, click and enter NICs, select the checkbox
            nic_status = self.get_text(nic_sending_link)
            time.sleep(self.SLEEP_TIME)
            if nic_status == "Inactive":
                self.click(nic_link)
                time.sleep(self.SLEEP_TIME)

                #click the "Connection automacically" check-box
                self.click(self.CONNECT_AUTOMATICALLY_CHECK_BOX)
                time.sleep(self.SLEEP_TIME)
        else:
            self.click(nic_link)
            time.sleep(self.SLEEP_TIME)

            #click the "Connection automacically" check-box
            self.click(self.CONNECT_AUTOMATICALLY_CHECK_BOX)
            time.sleep(self.SLEEP_TIME)

        return

    #check ifcfg-$NIC files via RHVH shell
    def _check_ifcfg_files_via_shell(self, ifcfg_files_name):
        ifcfg_file = self.host.execute(self.config_dict['check_ifcfg'], timeout=self.ENTER_SYSTEM_TIMEOUT)
        for ifcfg_file_name in ifcfg_files_name:
            if ifcfg_file_name not in ifcfg_file[1]:
                self.fail("The ifcfg file '{}' is not in RHVH shell.".format(ifcfg_file_name))
                return False

    
    #configure one nic IPv4 and IPv6 with specified mode
    def _configure_one_nic_ipv4_ipv6_with_specified_mode(
        self, nic_link=None, nic_sending_link=None,
        ipv4_mode_name=None, ipv4_mode_link=None, 
        ipv6_mode_name=None, ipv6_mode_link=None):

        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        #get NIC status and enter NIC link
        eno_status = self.get_text(nic_sending_link)
        self.click(nic_link)
        time.sleep(self.SLEEP_TIME)

        if eno_status == "Inactive":
            #turn on the NIC
            self.click(self.NETWORK_NICS_ON)
            time.sleep(self.SLEEP_TIME)

        #setting IPv4 to specified mode
        if ipv4_mode_link is not None and ipv4_mode_name is not None:
            self._ipv4_settings_config_mode(ipv4_mode_name, ipv4_mode_link)

        #setting IPv6 to specified mode
        if ipv6_mode_link is not None and ipv6_mode_name is not None:
            self._ipv6_settings_config_mode(ipv6_mode_name, ipv6_mode_link)

        #check if NICs configuration are correct
        self._check_nic_mode_settings(ipv4_mode_name, ipv6_mode_name)

        return


    #Clean up the test environment - delete vlan over bond, then delete bond
    def _clean_up_test_environment_vlan_over_bond(self):
        #Clean up the test environment-delete VLAN over bond
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #Click the Networking button on the left side of the page
        self.driver.switch_to.default_content()
        self.switch_to_frame(self.NETWORKING_FRAME)
        time.sleep(self.SLEEP_TIME)

        #Clean up the test environment-delete bond
        self.click(self.NETWORK_INFO_NICS_BOND_IP_ADDRESS)
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)
        return


    #create a vlan, then setting vlan's IPv4 and IPv6 mode
    def _create_vlan_and_setting_mode(
        self, parent_link, vlan_ip_address_link,
        ipv4_mode_name=None, ipv4_mode_link=None, 
        ipv6_mode_name=None, ipv6_mode_link=None):

        #click the "Add VLAN" button
        self.click(self.ADD_VLAN_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #select "Parent"
        self.click(self.VLAN_SETTING_PARENT_LIST)
        self.click(parent_link)
        time.sleep(self.SLEEP_TIME)

        #input "VLAN Id"
        self.input_text(self.VLAN_SETTING_VLAN_ID, self.config_dict['vlan_id'])
        time.sleep(self.SLEEP_TIME)

        #click the "Apply" button
        self.click(self.VLAN_SETTING_APPLY_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #click the link of VLAN to setting VLAN
        self.click(vlan_ip_address_link)
        time.sleep(self.SLEEP_TIME)

        #setting IPv4 to specified mode
        if ipv4_mode_link is not None and ipv4_mode_name is not None:
            self._ipv4_settings_config_mode(ipv4_mode_name, ipv4_mode_link)

        #setting IPv6 to specified mode
        if ipv6_mode_link is not None and ipv6_mode_name is not None:
            self._ipv6_settings_config_mode(ipv6_mode_name, ipv6_mode_link)

        return True


    #create a bond over local NICs eno3 and eno4, then setting IPv4 and IPv6 mode of the bond
    def _create_bond_and_setting_mode(
        self, ipv4_mode_name=None, ipv4_mode_link=None, 
        ipv6_mode_name=None, ipv6_mode_link=None):

        #click the "Add Bond" button
        self.click(self.ADD_BOND_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #input bond name
        self.input_text(self.BOND_SETTING_NAME, self.config_dict['ipv6_bond_setting_name'])
        time.sleep(self.SLEEP_TIME)

        #select Members of bond
        self.click(self.BOND_SETTING_MEMBERS_CHECKBOX_ENO3)
        self.click(self.BOND_SETTING_MEMBERS_CHECKBOX_ENO4)
        time.sleep(self.SLEEP_TIME)

        #select MAC address
        self.click(self.BOND_SETTING_MAC_LIST)
        self.click(self.BOND_SETTING_MAC_ENO3)
        time.sleep(self.SLEEP_TIME)

        #workaround-bug1817948-begin
        #select Mode
        self.click(self.BOND_SETTING_MODE)
        time.sleep(self.SLEEP_TIME)
        self.click(self.BOND_SETTING_MODE_XOR)
        time.sleep(self.SLEEP_TIME)
        self.click(self.BOND_SETTING_MODE)
        time.sleep(self.SLEEP_TIME)
        self.click(self.BOND_SETTING_MODE_ACTIVE_BACKUP)
        time.sleep(self.SLEEP_TIME)
        #workaround-bug1817948-end

        #select Primary NIC
        self.click(self.BOND_SETTING_PRIMARY_LIST)
        time.sleep(self.SLEEP_TIME)
        self.click(self.BOND_SETTING_PRIMARY_ENO3)
        time.sleep(self.SLEEP_TIME)

        #click the "Apply" button
        self.click(self.BOND_SETTING_APPLY)
        time.sleep(self.SLEEP_TIME)

        #click the link of bond to setting bond
        self.click(self.NETWORK_INFO_NICS_BOND_IP_ADDRESS)
        time.sleep(self.SLEEP_TIME)

        #check bond mode after bond created
        bond_mode_name = self.get_text(self.BOND_MODE_UNDER_BOND_NAME)
        if not (bond_mode_name == "Active backup"):
            self.fail("Bond mode error: Bond mode is not Active Backup.")
            return False

        #setting IPv4 to specified mode
        if ipv4_mode_link is not None and ipv4_mode_name is not None:
            self._ipv4_settings_config_mode(ipv4_mode_name, ipv4_mode_link)

        #setting IPv6 to specified mode
        if ipv6_mode_link is not None and ipv6_mode_name is not None :
            self._ipv6_settings_config_mode(ipv6_mode_name, ipv6_mode_link)

        return True

    
    #create a bond over selected NICs, then setting IPv4 and IPv6 mode of the bond
    def _create_bond_over_selected_nics_and_setting_mode(
        self, member1_link, member2_link, mac_link, primary_link,
        ipv4_mode_name=None, ipv4_mode_link=None, 
        ipv6_mode_name=None, ipv6_mode_link=None):

        #click the "Add Bond" button
        self.click(self.ADD_BOND_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #input bond name
        self.input_text(self.BOND_SETTING_NAME, self.config_dict['ipv6_bond_setting_name'])
        time.sleep(self.SLEEP_TIME)

        #select Members of bond
        self.click(member1_link)
        self.click(member2_link)
        time.sleep(self.SLEEP_TIME)

        #select MAC address
        self.click(self.BOND_SETTING_MAC_LIST)
        self.click(self.mac_link)
        time.sleep(self.SLEEP_TIME)

        #select Primary NIC
        self.click(self.BOND_SETTING_PRIMARY_LIST)
        time.sleep(self.SLEEP_TIME)
        self.click(self.primary_link)
        time.sleep(self.SLEEP_TIME)

        #click the "Apply" button
        self.click(self.BOND_SETTING_APPLY)
        time.sleep(self.SLEEP_TIME)

        #click the link of bond to setting bond
        self.click(self.NETWORK_INFO_NICS_BOND_IP_ADDRESS)
        time.sleep(self.SLEEP_TIME)

        #setting IPv4 to specified mode
        if ipv4_mode_link is not None and ipv4_mode_name is not None:
            self._ipv4_settings_config_mode(ipv4_mode_name, ipv4_mode_link)

        #setting IPv6 to specified mode
        if ipv6_mode_link is not None and ipv6_mode_name is not None :
            self._ipv6_settings_config_mode(ipv6_mode_name, ipv6_mode_link)

        return True


    #check if IPv4 and IPv6 mode settings are correct
    def _check_nic_mode_settings(self, IPv4_mode_name=None, Ipv6_mode_name=None):
        if IPv4_mode_name is not None:
            #check if IPv4 of NIC is in correct mode
            IPv4_mode_name_from_cockpit = self.get_text(self.IPV4_MODE_NAME)
            if IPv4_mode_name == self.config_dict['IPv4_mode_manual']:
                self.assertEqual(self.config_dict['ipv4_ip_link_name'], IPv4_mode_name_from_cockpit,
                "Configure error. Bond IPv4 is not on '{}' mode.".format(IPv4_mode_name))
            else:
                self.assertEqual(IPv4_mode_name, IPv4_mode_name_from_cockpit,
                "Configure error. Bond IPv4 is not on '{}' mode.".format(IPv4_mode_name))

        if Ipv6_mode_name is not None:
            #check if IPv6 of NIc is in correct mode
            IPv6_mode_name_from_cockpit = self.get_text(self.IPV6_MODE_NAME)
            if Ipv6_mode_name == self.config_dict['IPv6_mode_manual']:
                self.assertEqual(self.config_dict['ipv6_ip_link_name'], IPv6_mode_name_from_cockpit,
                "Configure error. Bond IPv6 is not on '{}' mode.".format(Ipv6_mode_name))
            else:
                self.assertEqual(Ipv6_mode_name, IPv6_mode_name_from_cockpit,
                "Configure error. Bond IPv6 is not on '{}' mode.".format(Ipv6_mode_name))

        return


    #check if IPv4 and IPv6 mode settings are correct after reboot
    def _check_nic_mode_settings_after_reboot(self, nic_link, ipv4_mode_name=None, ipv6_mode_name=None):
        #return to default html frame
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)

        #click NICs link enter NICs page again
        self.click(nic_link)
        time.sleep(self.SLEEP_TIME)

        #check if NICs configuration are correct
        self._check_nic_mode_settings(ipv4_mode_name, ipv6_mode_name)

        return


    #check if IPv4 and IPv6 mode settings are correct before and after reboot
    def _check_nic_mode_before_and_after_reboot(self,nics_link, IPv4_mode_name=None, Ipv6_mode_name=None):
        #check IPv4 and IPv6 configuration before rebooting
        self._check_nic_mode_settings(IPv4_mode_name, Ipv6_mode_name)

        #reboot system and login cockpit again
        self._reboot_and_login_in_again()

        #return to default html frame
        self.driver.switch_to.default_content()
        self.switch_to_frame(self.NETWORKING_FRAME)

        #click NICs link enter NICs page again
        self.click(nics_link)
        time.sleep(self.SLEEP_TIME)

        #after reboot, check if IPv4 of NIC is in correct mode
        if IPv4_mode_name is not None:
            IPv4_mode_name_reboot = self.get_text(self.IPV4_MODE_NAME)
            if IPv4_mode_name == self.config_dict['IPv4_mode_manual']:
                self.assertEqual(self.config_dict['ipv4_ip_link_name'], IPv4_mode_name_reboot,
                "Configurations are not persisted. Bond IPv4 is not on '{}' mode.".format(IPv4_mode_name))
            else:
                self.assertEqual(IPv4_mode_name, IPv4_mode_name_reboot,
                "Configurations are not persisted. Bond IPv4 is not on '{}' mode.".format(IPv4_mode_name))
                
        #after reboot, check if IPv6 of NIC is in correct mode
        if Ipv6_mode_name is not None:
            IPv6_mode_name_reboot = self.get_text(self.IPV6_MODE_NAME)
            if Ipv6_mode_name == self.config_dict['IPv6_mode_manual']:
                self.assertEqual(self.config_dict['ipv6_ip_link_name'], IPv6_mode_name_reboot,
                "Configurations are not persisted. Bond IPv6 is not on '{}' mode.".format(Ipv6_mode_name))
            else:
                self.assertEqual(Ipv6_mode_name, IPv6_mode_name_reboot,
                "Configurations are not persisted. Bond IPv6 is not on '{}' mode.".format(Ipv6_mode_name))

        return
    
    #Delete bond via bond link
    def _clean_environment_delete_bond_vlan(self, bond_vlan_link):
        #return to default html frame
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)

        #click NICs link enter NICs page again
        self.click(bond_vlan_link)
        time.sleep(self.SLEEP_TIME)

        #click the "Delete" button       
        self.click(self.BOND_VLAN_DELETE_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return

    #Delete manually set IPs
    def _clean_environment_delete_manual_ip(self, nic_link, ipv4_ipv6_link):
        #return to default html frame
        self.driver.switch_to.default_content()
        self.click(self.NETWORKING_MENU_LEFT_SIDE)
        self.switch_to_frame(self.NETWORKING_FRAME)

        #click NICs link enter NICs page again
        self.click(nic_link)
        time.sleep(self.SLEEP_TIME)

        #click ipv4/ipv6 link enter IPv4/IPv6 Settings page       
        self.click(ipv4_ipv6_link)
        time.sleep(self.SLEEP_TIME)

        #click "Automatic" mode
        self.click(self.IPV6_SETTING_DROP_DOWN_LIST)
        self.click(self.IPV6_SETTING_DROP_DOWN_LIST_AUTOMATIC)
        time.sleep(self.SLEEP_TIME)

        #click the "-" button to delete the manual IP
        self.click(self.IPV6_SETTING_DELETE_MANUAL_IP_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #click the "Apply" button
        self.click(self.IPV6_SETTING_APPLY_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return


    #change mode in the "IPv6 Settings" page
    def _ipv6_settings_config_mode(self, mode_name, mode_link):
       
        #click ipv6 link enter IPv6 Settings page       
        self.click(self.IPV6_CONFIG_LINK)
        time.sleep(self.SLEEP_TIME)
        self.click(self.IPV6_SETTING_DROP_DOWN_LIST)
        self.click(mode_link)
        time.sleep(self.SLEEP_TIME)

        if mode_name == self.config_dict['IPv6_mode_manual']:
            #input ip address of manual mode
            self.input_text(self.INPUT, self.config_dict['ipv6_ip_manual'])
            self.input_text(self.INPUT_PREFIX, self.config_dict['ipv6_prefix_length'])
            time.sleep(self.SLEEP_TIME)

        #click the "Apply" button
        self.click(self.IPV6_SETTING_APPLY_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return True


    #change mode in the "IPv4 Settings" page
    def _ipv4_settings_config_mode(self, mode_name, mode_link):

        #click IPv4 link enter "IPv4 settings" page
        self.click(self.IPV4_CONFIG_LINK)
        time.sleep(self.SLEEP_TIME)
        self.click(self.IPV4_SETTING_DROP_DOWN_LIST)
        self.click(mode_link)
        time.sleep(self.SLEEP_TIME)

        if mode_name == self.config_dict['IPv4_mode_manual']:
            #input ip address of manual mode
            self.input_text(self.INPUT, self.config_dict['ipv4_ip_manual'])
            self.input_text(self.INPUT_PREFIX, self.config_dict['ipv4_prefix_length'])
            time.sleep(self.SLEEP_TIME)

        #click the "Apply" button
        self.click(self.IPV6_SETTING_APPLY_BUTTON)
        time.sleep(self.SLEEP_TIME)

        return True


    #check ipv6 ip via cockpit
    def _check_ipv6_ip(self, element_path):
        #switch to the networking frame
        self.driver.switch_to.default_content()
        self.switch_to_frame(self.NETWORKING_FRAME)
        current_ipv6_ip_text = self.config_dict['ipv6_ip_in_cockpit']
        self.assertEqual(self._get_current_ipv6_ip_text(element_path), current_ipv6_ip_text,
        'The current IPV6 IP address is inconsistent with the configuration.')


    #get IPv6 ip from cockpit
    def _get_current_ipv6_ip_text(self, element_path):
        ip_addresses = self.get_text(element_path)
        if "," in ip_addresses:
            ipv6_ip = ip_addresses.split(', ')[1]
            return ipv6_ip
        else:
            if ip_addresses.startswith("2001") or ip_addresses.startswith("2620"):
                return ip_addresses
            else:
                return ""
    

    #get IPv4 ip from cockpit
    def _get_current_ipv4_ip_text(self, element_path):
        ip_addresses = self.get_text(element_path)
        if "," in ip_addresses:
            ipv4_ip = ip_addresses.split(', ')[0]
            return ipv4_ip
        else:
            if ip_addresses.startswith("192") or ip_addresses.startswith("10"):
                return ip_addresses
            else:
                return ""


    #run command "ip a s" via rhvh shell, and returns the string containing the ip
    #parameters: (nic_name: eno1, eno2, eno3, eno4...), (net_type: "IPv4" or "IPv6")
    def _get_ip_via_rhvh_shell(self,nic_name,net_type):
        time.sleep(self.WAIT_IP_READY)

        key_in_dict = "get_ip_" + nic_name + "_" + net_type
        cmd = self.config_dict[key_in_dict]
        if not cmd:
            self.fail("The key '{}' is not in networking_config.yml".format(key_in_dict))
            return ""
        
        ip_a_s = self.host.execute(cmd, timeout=self.ENTER_SYSTEM_TIMEOUT)
        if not ip_a_s[0]:
            return ""
        else:
            if ip_a_s[1]:
                    return ip_a_s[1]
            else:
                return ""
        

    #reboot system and login cockpit via browser
    def _reboot_and_login_in_again(self):
        #reboot the system
        self._reboot_system()

        #After rebooting, check the system until the reboot is successful
        ret = self._wait_system_reboot_ready()
        if not ret[0]:
            return False

        # #add ip route
        # self.host.execute(self.config_dict['add_route'], timeout=self.ENTER_SYSTEM_TIMEOUT)
        # time.sleep(self.WAIT_IP_READY)

        #login to cockpit again 
        #self.setUp()

        #click the "Reconnect" button
        self.driver.switch_to.default_content()
        self.click(self.RECONNECT_BUTTON)
        
        #login to cockpit again
        username = os.environ.get('USERNAME')
        passwd = os.environ.get('PASSWD')
        self.login(username, passwd)
        time.sleep(self.SLEEP_TIME)

        #click "Networking" menu on left side
        self.click(self.NETWORKING_MENU)
        time.sleep(self.SLEEP_TIME)

    #add ip route
    def _add_10_route(self):
        target_ip = self.config_dict['add_route']

        progress_log.info("Start to add %s route on host...", target_ip)

        #cmd = "ip route | grep --color=never default | head -1"
        cmd = "ip route | grep --color=never default | grep -v 192. | head -1"#workaround for RHVH4.4, because route can not persisted

        ret = self.host.execute(cmd, timeout=self.ENTER_SYSTEM_TIMEOUT)
        if not ret[0]:
            self.fail("Get default pub route failed.")
            return False
        progress_log.info('The default pub route is "%s"', ret[1])

        gateway = ret[1].split()[2]
        nic = ret[1].split()[4]

        cmd = "ip route add {target_ip} via {gateway} dev {nic}".format(
            target_ip=target_ip, gateway=gateway, nic=nic)
        ret = self.host.execute(cmd, timeout=self.ENTER_SYSTEM_TIMEOUT)
        if not ret[0]:
            self.fail("Add %s to route table failed.", target_ip)
            return False

        cmd = "echo '{target_ip} via {gateway}' > /etc/sysconfig/network-scripts/route-{nic}".format(
            target_ip=target_ip, gateway=gateway, nic=nic)
        ret = self.host.execute(cmd, timeout=self.ENTER_SYSTEM_TIMEOUT)
        if not ret[0]:
            self.fail("Create route-%s file failed.", nic)
            return False

        progress_log.info("Add %s route on host finished.", target_ip)
        return True
    
    #click "System -> Power Options Restart" to reboot system
    def _reboot_system(self):
        #switch to the root html and click the "system" button
        self.driver.switch_to.default_content()
        self.click(self.SYSTEM_MENU)
        time.sleep(self.SLEEP_TIME)
        
        #switch to the system frame
        self.driver.switch_to.default_content()
        self.switch_to_frame(self.SYSTEM_FRAME)
        self.click(self.SYSTEM_RESTART_BUTTON)
        time.sleep(self.SLEEP_TIME)

        #click 1 Minute -> No Delay -> Restart
        self.click(self.SYSTEM_RESTART_DELAY_1_MINUTE)
        time.sleep(self.SLEEP_TIME)
        self.click(self.SYSTEM_RESTART_DELAY_NO_DELAY)
        self.click(self.SYSTEM_RESTART_RESTART_BUTTON)


    #Wait for the system reboot finished
    def _wait_system_reboot_ready(self):
        count = 0
        while (count < self.ENTER_SYSTEM_MAXCOUNT):
            time.sleep(self.ENTER_SYSTEM_INTERVAL)
            ret = self.host.execute("imgbase w", timeout=self.ENTER_SYSTEM_TIMEOUT)
            if not ret[0]:
                count = count + 1
            else:
                break

        return ret


    #add host to RHVM and then check network status
    def _add_host_to_rhvm(self, is_vlan=False):
        progress_log.info("Add host to rhvm...")

        config_dict_pass = yaml.load(open('./config.yml'), Loader=yaml.FullLoader)

        # get rhvm fqdn
        _rhvm_fqdn= self._get_rhvm_fqdn()
        if not _rhvm_fqdn:
            self.fail("Get RHVM FQDN failed when adding host to RHVH.")
            return False

        # get host ip, vlanid
        _host_ip = self._get_host_ip(is_vlan)
        if not _host_ip:
            self.fail("Get host IP failed when adding host to RHVH.")
            return False

        # get host cpu type
        _host_cpu_type = self._get_host_cpu_type()
        if not _host_cpu_type:
            self.fail("Get host cpu type failed when adding host to RHVH.")
            return False

        #get host password
        _host_pass = config_dict_pass['host_pass']
        if not _host_pass:
            self.fail("Get host password failed when adding host to RHVH.")
            return False

        progress_log.info(
            "rhvm: %s, datacenter: %s, cluster_name: %s, host_name: %s, host_ip: %s, cpu_type: %s",
            _rhvm_fqdn, self.RHVM_COMPUTE_MAP.get("dc_name"), self.RHVM_COMPUTE_MAP.get("cluster_name"),
            self.RHVM_COMPUTE_MAP.get("host_name"), _host_ip,
            _host_cpu_type)

        try:
            #self._rhvm = RhevmAction(_rhvm_fqdn)
            self._rhvm = BaseRhvAPI(_rhvm_fqdn)

            self._del_host_on_rhvm()

            progress_log.info("Add datacenter %s", self.RHVM_COMPUTE_MAP.get("dc_name"))
            self._rhvm.add_data_center(self.RHVM_COMPUTE_MAP.get("dc_name"), local=False, wait=True)

            progress_log.info("Add cluster %s", self.RHVM_COMPUTE_MAP.get("cluster_name"))
            self._rhvm.add_cluster(self.RHVM_COMPUTE_MAP.get("cluster_name"), data_center_name=self.RHVM_COMPUTE_MAP.get("dc_name"), cpu_type=_host_cpu_type)


            self._rhvm.add_host(self.RHVM_COMPUTE_MAP.get("host_name"), address=_host_ip, root_password=_host_pass,
                                cluster_name=self.RHVM_COMPUTE_MAP.get("cluster_name"), deploy_hosted_engine=False)
        except Exception as e:
            progress_log.error(e)
            return False

        progress_log.info("Add host to rhvm finished.")
        return True


    def _get_rhvm_fqdn(self):
        #switch to the root html and click the "system" button
        self.driver.switch_to.default_content()
        self.click("//a[@href='/system']")
        time.sleep(self.SLEEP_TIME)
        
        #switch to the system frame
        self.driver.switch_to.default_content()
        self.switch_to_frame("cockpit1:localhost/system")
        system_version = self.get_text(self.SYSTEM_VERSION)
        progress_log.info("The system version is: '{}'",system_version)
        time.sleep(self.SLEEP_TIME)

        if ' 4.0' in system_version:
            key = "4.0_rhvm_fqdn"
        elif ' 4.1' in system_version:
            key = "4.1_rhvm_fqdn"
        elif ' 4.2' in system_version:
            key = "4.2_rhvm_fqdn"
        elif ' 4.3' in system_version:
            key = "4.3_rhvm_fqdn"
        elif ' 4.4' in system_version:
            key = "4.4_rhvm_fqdn"
        elif ' 4.5' in system_version:
            key = "4.5_rhvm_fqdn"
        else:
            progress_log.error("The version of host src build is not 4.0 or 4.1 or 4.2 or 4.3 or 4.4.x")
            return
        _rhvm_fqdn = self.RHVM_DATA_MAP.get(key)
        return _rhvm_fqdn


    def _get_host_ip(self, is_vlan):
        progress_log.info("Get host ip...")

        cmd = "ip -f inet addr show | grep 'inet 10.73.' | awk '{print $2}'| awk -F '/' '{print $1}' | awk 'NR==1{print}'"
        ret = self.host.execute(cmd, timeout=self.FABRIC_TIMEOUT)
        if not ret[0]:
            return
        return ret[1]


    def _get_host_cpu_type(self):
        progress_log.info("Get host cpu type...")
        cmd = 'lscpu | grep "Model name"'
        ret = self.host.execute(cmd, timeout=self.ENTER_SYSTEM_TIMEOUT)
        progress_log.info("Get host cpu type...ret...%s",ret[1])
        if ret[0]:
            if "AMD" in ret[1]:
                cpu_type = "AMD EPYC"
            elif "Intel" in ret[1]:
                cpu_type = "Intel Nehalem Family"
            else:
                cpu_type = None
        else:
            cpu_type = None
        progress_log.info("Get host cpu type...2...%s",cpu_type)
        return cpu_type

    # check host status on RHVM
    def _check_host_status_on_rhvm(self):

        if not self.RHVM_COMPUTE_MAP.get("host_name"):
            return True

        progress_log.info("Check host status on rhvm.")

        count = 0
        while (count < self.CHK_HOST_ON_RHVM_STAT_MAXCOUNT):
            host = self._rhvm.find_host(self.RHVM_COMPUTE_MAP.get("host_name"))
            host_status = self._rhvm.current_host_status(self.RHVM_COMPUTE_MAP.get("host_name"))
            
            if host and str(host_status) == 'up':
                break
            count = count + 1
            time.sleep(self.CHK_HOST_ON_RHVM_STAT_INTERVAL)
        else:
            progress_log.error("Host is not up on rhvm.")
            return False
        progress_log.info("Host is up on rhvm.")
        return True

    #delete host on RHVM
    def _del_host_on_rhvm(self):
        # get rhvm fqdn
        _rhvm_fqdn= self._get_rhvm_fqdn()
        if not _rhvm_fqdn:
            return False

        self._rhvm_clean = BaseRhvAPI(_rhvm_fqdn)
        if not self._rhvm_clean:
            return False

        count = 0
        while (count < 3):
            try:
                if self.RHVM_COMPUTE_MAP.get("host_name"):
                    progress_log.info("Try to remove host %s", self.RHVM_COMPUTE_MAP.get("host_name"))

                    #peyu 20200519-begin
                    host = self._rhvm_clean.find_host(self.RHVM_COMPUTE_MAP.get("host_name"))
                    host_status = self._rhvm_clean.current_host_status(self.RHVM_COMPUTE_MAP.get("host_name"))
                    time.sleep(2)

                    if host and str(host_status) == 'up':
                        self._rhvm_clean.deactivate_host(self.RHVM_COMPUTE_MAP.get("host_name"))
                        time.sleep(10)
                    #peyu 20200519-end

                    self._rhvm_clean.del_host(self.RHVM_COMPUTE_MAP.get("host_name"))

                if self.RHVM_COMPUTE_MAP.get("cluster_name"):
                    progress_log.info("Try to remove cluster %s", self.RHVM_COMPUTE_MAP.get("cluster_name"))
                    self._rhvm_clean.del_cluster(self.RHVM_COMPUTE_MAP.get("cluster_name"))

                if self.RHVM_COMPUTE_MAP.get("dc_name"):
                    progress_log.info("Try to remove data_center %s", self.RHVM_COMPUTE_MAP.get("dc_name"))
                    self._rhvm_clean.del_data_center(self.RHVM_COMPUTE_MAP.get("dc_name"))
            except Exception as e:
                progress_log.error(e)
                time.sleep(20)
                count = count + 1
            else:
                break
