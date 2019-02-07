#!/usr/bin/python3

import json,requests,csv,os
import ipaddress
from aruba_api_caller import *


#variable definition
csv_filename = 'shop-list.txt'
json_filename = 'shop-list.json'
cwd = os.getcwd()

#Display current working directory
print ('Current Working Directory is: ' + cwd)

#fetch current VLAN 4094 IP

#check if IP belongs to subnet
iface = ipaddress.ip_interface('10.110.224.103/28')
nwaddr = iface.network.network_address
print (nwaddr)

#ipaddress.ip_address('10.110.224.103') in ipaddress.ip_network('10.110.224.96/28')