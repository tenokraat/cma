#!/usr/bin/python3

import json,requests,csv,os
from aruba_api_caller import *


def readCSV(nw_addr):
    #variable definition
    csv_filename = 'cma-shop-list.txt'

    #Open CSV in Read-only mode
    csv_file = open(csv_filename, 'r')
    reader = csv.reader(csv_file)

    #Create empty dictionary
    shops = {}

    #Headers in CSV: network-address,sap-id,street,zip,place,state

    #Read all lines in CSV and put them in the dictionary
    for row in reader:
        shops[row[0]] = {'sap-id':row[1], 'street':row[2], 'zip':row[3], 'place':row[4], 'state':row[5]}

    print('The new controller name is: ' + shops[nw_addr]['sap-id']+'-'+shops[nw_addr]['place']+'-'+shops[nw_addr]['state'])