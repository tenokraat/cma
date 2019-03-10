#!/usr/bin/python3

import json,requests,re,csv,os
import ipaddress
from aruba_api_caller import *

#User Input
#vmm_hostname = input ('VMM Hostname or IP: ')
#admin_user = input('Enter username: ')
#admin_password = input(f'Enter {admin_user} password: ')

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[3] == valueToFind:
            listOfKeys.append(item[4])
    return  listOfKeys

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

def get_uplink_ip(mac_addr):

    req = session.get('configuration/object/int_vlan', f'/md/hpe-ch/zuo01-mc/{mac_addr}')

    res = dict()
    res = extract_values(req, 'ipaddr')

    for element in res:
        match_result = re.match('^192.168.', element)

        if match_result:
            print (match_result.group(1))


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


session = api_session('192.168.65.95', 'admin', 'Adminhpq-123', check_ssl=False)

session.login()

cd = session.get('configuration/object/node_hierarchy')

get_uplink_ip('00:1a:1e:00:5d:e0')

session.logout()
