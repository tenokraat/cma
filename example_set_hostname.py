#!/usr/bin/python3

import json,requests,csv,os
from aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")
new_hostname = {"hostname": "cs-aruba-vmc2"}

session.login()

hostname_json = session.get("configuration/object/hostname", "/md/HPE-CH/ZUO01-VMC/00:50:56:ab:1a:81")
print(hostname_json)

curr_hostname = hostname_json['_data']['hostname']['hostname']
print(curr_hostname)

session.post("configuration/object/hostname", new_hostname, "/md/HPE-CH/ZUO01-VMC/00:50:56:ab:1a:81")

session.write_memory("/md/HPE-CH/ZUO01-VMC/00:50:56:ab:1a:81") 

hostname_json = session.get("configuration/object/hostname", "/md/HPE-CH/ZUO01-VMC/00:50:56:ab:1a:81")
curr_hostname = hostname_json['_data']['hostname']['hostname']
print(curr_hostname)
  
session.logout()