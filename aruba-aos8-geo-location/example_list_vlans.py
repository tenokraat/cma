#!/usr/bin/python3

import json,requests
from .aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")

session.login()

VLANS = session.get("configuration/container/Interfaces", "/md")

for VLAN in VLANS["_data"]["vlan_id"]:
	print ("VLAN-ID: " + str(VLAN["id"]))
	if "vlan_id__descr" in VLAN:
		print ("Description: " + VLAN["vlan_id__descr"]["descr"])

session.logout()
