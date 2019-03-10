#!/usr/bin/python3

import json,requests,csv,os
from aruba_api_caller import *

def set_hostname(new_hostname, mac_addr):

    hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = hostname_json['_data']['hostname']['hostname']

    print('Controller' + curr_hostname + ' will now be renamed to ' + new_hostname)

    session.post('configuration/object/hostname', new_hostname, f'/md/cma/shops/{mac_addr}')

    session.write_memory(f'/md/cma/shops/{mac_addr}') 

    hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = hostname_json['_data']['hostname']['hostname']

    print ('Controller successfully renamed to ' + curr_hostname)