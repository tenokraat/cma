#!/usr/bin/python3

import json,requests,csv,os
import ipaddress
from aruba_api_caller import *

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
