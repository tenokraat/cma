#!/usr/bin/python3

import json,requests
from aruba_api_caller import *

session = api_session("192.168.230.23", "admin", "Aruba1234")

session.login()

show_switches = session.get("configuration/showcommand?command=show+switches", "")

print (show_switches)

session.logout()

