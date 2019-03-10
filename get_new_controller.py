#!/usr/bin/python3

import json,requests,re,csv,os
import ipaddress
from check_address import *
from aruba_api_caller import *

#User Input
#vmm_hostname = input ('VMM Hostname or IP: ')
#admin_user = input('Enter username: ')
#admin_password = input(f'Enter {admin_user} password: ')

#Session Credentials
session = api_session('192.168.65.95', 'admin', 'Adminhpq-123', check_ssl=False)

session.login()

cd = session.get('configuration/object/node_hierarchy')

def check_new_device():

    #Check node hierarchy for devices that have not been renamed, yet.
    for each in cd['childnodes'][1]['childnodes'][1]['childnodes'][2]['devices']:
        currHostname = each['name']
            
        if 'CTRL_' in currHostname:
            isDefault = True
            print('New device detected.')
        else:
            isDefault = False 

        if isDefault == True:
            mac_addr = each['mac']
            print ('Hostname: '+each['name']+' MAC: '+each['mac'])

        else:
            pass

def get_uplink_ip():

    intdata = dict()

    req = session.get('configuration/object/int_vlan', f'/md/hpe-ch/zuo01-mc/{mac_addr}')
    res = req.json()
    result = res['int_vlan']

    intdata = json.loads(res)
 



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
       
session.logout()
