#!/usr/bin/python3

import json,requests
from aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")
isEmpty = False

session.login()

cd = session.get("configuration/object/node_hierarchy")

#def checkNewDevices():
#Check node hierarchy for devices that have not been renamed, yet.
for each in cd['childnodes'][1]['childnodes'][1]['childnodes'][1]['devices']:
    if each['name'] == each['mac']:
     print ('Hostname: '+each['name']+' MAC: '+each['mac'])
    else:
        isEmpty = True

if isEmpty: 
    print ('No new devices found.')
else:
    print('There are new devices detected.')
  
session.logout()
