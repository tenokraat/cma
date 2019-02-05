#!/usr/bin/python3

import json,requests
from aruba_api_caller import *

session = api_session("cs-aruba-mm.hpearubademo.com", "admin", "Adminhpq-123")

session.login()

show_switches = session.get("configuration/showcommand?command=show+switches", "")

print (show_switches)

session.logout()

