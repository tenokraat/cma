#!/usr/bin/python3

import json,requests
from aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")

session.login()

cd = session.get("configuration/object/node_hierarchy")

output = cd['name']

print ('Node Hierarchy Name: '+output)

#md_name = cd['childnodes'][1]['childnodes'][1]['childnodes'][1]['devices']

for each in cd['childnodes'][1]['childnodes'][1]['childnodes'][1]['devices']:
    print (each['name']) 
    print(each['mac'])

#print (md_name)

session.logout()
