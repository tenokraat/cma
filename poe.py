#!/usr/bin/python3

import json,requests,re,csv,os,sys,time
from aruba_api_caller import *

## MM Login Credentials ##

vmm_hostname = '192.168.230.23'
admin_user = 'python'
admin_password = 'Aruba1234'

def set_int_poe(mac_addr):
    int_gig_no = 7

    int_poe_json = {"_data": { "int_gig": { f"{int_gig_no}": {"int_gig_poe": {"_flags": {"inherited": "true"}}}}}}

    session.post('configuration/object/int_gig', int_poe_json, f'/md/cma/shops/{mac_addr}')

    session.write_memory(f'/md/cma/shops/{mac_addr}')

#Instantiate API session variable
session = api_session(vmm_hostname, admin_user, admin_password, check_ssl=False)

session.login()

set_int_poe('20:4c:03:21:af:5c')