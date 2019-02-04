#!/usr/bin/python3

import json,requests
from aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")

session.login()

cd = session.get("configuration/object/node_hierarchy")

print (cd)

session.logout()
