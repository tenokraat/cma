#!/usr/bin/python3

import json,requests
#from check_address import *
from aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")

session.login()

vlan_interface = session.get("configuration/object/int_vlan", "/md/hpe-ch/zuo01-mc/cs-aruba-7210-mc1")

print (vlan_interface)

session.logout()