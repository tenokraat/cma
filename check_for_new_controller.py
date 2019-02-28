#!/usr/bin/python3

import json,requests,re
from check_address import *
from aruba_api_caller import *

#User Input
#vmm_hostname = input ('VMM Hostname or IP: ')
#admin_user = input('Enter username: ')
#admin_password = input(f'Enter {admin_user} password: ')

#Session Credentials
session = api_session('192.168.230.23', 'admin', 'Aruba1234', check_ssl=False)

session.login()

cd = session.get("configuration/object/node_hierarchy")

#def checkNewDevices():
#Check node hierarchy for devices that have not been renamed, yet.
for each in cd['childnodes'][1]['childnodes'][1]['childnodes'][2]['devices']:
    currHostname = each['name']
    print(currHostname)

    if 'CTRL_' in currHostname:
        isDefault = True
    else:
        isDefault = False 

    if isDefault == True:   
        print('There are new devices detected.')
        print ('Hostname: '+each['name']+' MAC: '+each['mac'])
    else:
        pass

if isDefault == False:
    print ('No new devices found.')

else:
    pass
       
session.logout()
