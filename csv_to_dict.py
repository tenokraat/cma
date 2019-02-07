#!/usr/bin/python3

import json,requests,csv,os
from aruba_api_caller import *

#variable definition
csv_filename = 'cma-shop-list.txt'

#Open CSV in Read-only mode
csv_file = open(csv_filename, 'r')
reader = csv.reader(csv_file)

#Create empty dictionary
shops = {}

#Headers in CSV: sap-id,street,zip,place,state,network-address

#Read all lines in CSV and put them in the dictionary
for row in reader:
    shops[row[0]] = {'street':row[1], 'zip':row[2], 'place':row[3], 'state':row[4], 'network-address':row[5]}

sap_id = input ('Enter SAP-ID: ')

choice = input ('What information would you like to find? ')

print(shops[sap_id][choice])