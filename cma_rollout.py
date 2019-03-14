#!/usr/bin/python3

import json,requests,re,csv,os
import ipaddress
from aruba_api_caller import *

#Login Credentials

vmm_hostname = '192.168.65.95'
admin_user = 'admin'
admin_password = 'Adminhpq-123'

#vmm_hostname = input ('VMM Hostname or IP: ')
#admin_user = input('Enter username: ')
#admin_password = input(f'Enter {admin_user} password: ')

#Get a list of keys from dictionary which has value that matches with any value in given list of values

def firmware_upgrade(mac_addr, aos_version):

    json_data = """ 
    {
        "img-version": "{aos_version}",
        "mac-addr": "{mac_addr}",
        "imagehost": "192.168.230.23",
        "username": "admin ",
        "image-path": ".",
        "passwd": "Aruba1234"
    }
    """

    json_obj = json.loads(json_data)

    session.post('configuration/object/upgrade_lcs_copy_scp_reboot', json_obj, f'/md/cma/shops/{mac_addr}')

def check_new_device():

    #Check node hierarchy for devices that have not been renamed, yet.
    node_hierarchy = session.get('configuration/object/node_hierarchy')

    #Define nested JSON data 
    ctrl_json = node_hierarchy['childnodes'][1]['childnodes'][1]['childnodes'][2]['devices']

    ctrl_list = list() #create list to append multiple new controllers
    
    for each in ctrl_json:
        currHostname = each['name']

        if 'CTRL_' in currHostname:
            isDefault = True
            print('New device detected.')

        else:
            isDefault = False 

        if isDefault == True:
            mac_addr = each['mac']
            #print ('Hostname: '+ each['name']+' MAC: '+ each['mac'] + '\n')
            ctrl_list.append(mac_addr)
        else:
            pass

    return ctrl_list

def get_uplink_ip(mac_addr):

    #cli_json = session.cli_command(f'show crypto-local ipsec-map tag default-local-master-ipsecmap-{mac_addr}-link1')
    cli_json = session.cli_command('show crypto-local ipsec-map tag default-psk-redundant-master-ipsecmap')

    for line in cli_json['_data']:

        m = re.match('^Destination network:', line)

        if  m is not None:
            sub_string = re.sub("Destination network: ", "", line)
            print (re.sub("Destination network: ", "", line))

            uplink_ip = ipaddress._split_optional_netmask(sub_string)
            print (uplink_ip[0])

            break

def check_shop_ip(uplink_ip):
    #variable definition
    csv_filename = 'shop-list.txt'
    json_filename = 'shop-list.json'
    cwd = os.getcwd()

    #Display current working directory
    print ('Current Working Directory is: ' + cwd)

    #check if IP belongs to subnet
    iface = ipaddress.ip_interface(f'{uplink_ip}/28')
    nwaddr = iface.network.network_address
    print (nwaddr)

    #if ipaddress.ip_address(uplink_ip) in nwaddr:

def set_hostname(new_hostname, mac_addr):

    hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = hostname_json['_data']['hostname']['hostname']

    print('Controller' + curr_hostname + ' will now be renamed to ' + new_hostname)

    session.post('configuration/object/hostname', new_hostname, f'/md/cma/shops/{mac_addr}')

    session.write_memory(f'/md/cma/shops/{mac_addr}') 

    hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = hostname_json['_data']['hostname']['hostname']

    print ('Controller successfully renamed to ' + curr_hostname)

session = api_session(vmm_hostname, admin_user, admin_password, check_ssl=False)

#cma test section
session.login()

new_ctrl = check_new_device()
print (new_ctrl)

#for md in new_ctrl:
#   get_uplink_ip(md)


session.logout()