#!/usr/bin/python3

import json,requests,re,csv,os,sys,time
from aruba_api_caller import *

## MM Login Credentials ##

vmm_hostname = '192.168.230.23'
admin_user = 'python'
admin_password = 'Aruba1234'

def set_int_poe(mac_addr):
    int_gig_no = 1

    int_poe_json = {"slot/module/port": f"0/0/{int_gig_no}", "int_gig_poe": {"cisco": "true"}}

    session.post('configuration/object/int_gig', int_poe_json, f'/md/cma/shops/{mac_addr}')

def get_devices():

    #Check MM node hierarchy for devices that have not been renamed, yet.
    node_hierarchy = session.get('configuration/object/node_hierarchy')

    #Define data from nested JSON that is retrieved (needs modification depending on hierarchy structure)
    ctrl_json = node_hierarchy['childnodes'][1]['childnodes'][0]['childnodes'][0]['devices']

    ctrl_list = list() #create list to append  controller mac addresses

    isExisting = False
    
    #Check each entry in JSON if it starts with 'CTRL_' and append to list if True
    for md in ctrl_json:
        currHostname = md['name']

        if '-' in currHostname:
            isExisting = True
            print('>>> Existing device detected: ' + currHostname) 

            mac_addr = md['mac']
            ctrl_list.append(mac_addr)

        else:
            pass
        
        if isExisting == False:
            print('>>> No existing devices found. <<<')

    #Return list of new controllers   
    return ctrl_list, isExisting

#Instantiate API session variable
session = api_session(vmm_hostname, admin_user, admin_password, check_ssl=False)

session.login()

ctrl_list, isExisting = get_devices()

print(ctrl_list)

for md in ctrl_list:
    
    print(md)
    ctrl_mac = md
    set_int_poe(ctrl_mac)

session.logout()