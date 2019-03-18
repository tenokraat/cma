#!/usr/bin/python3

import json,requests,re,csv,os,sys,time
import ipaddress
from aruba_api_caller import *

#Disable system-level proxy definition for requests
os.environ['no_proxy'] = '*'

#Login Credentials

vmm_hostname = '192.168.230.23'
admin_user = 'python'
admin_password = 'Aruba1234'

#vmm_hostname = input ('VMM Hostname or IP: ')
#admin_user = input('Enter username: ')
#admin_password = input(f'Enter {admin_user} password: ')

def firmware_upgrade(mac_addr, aos_compliance_version, scp_server, scp_user, scp_password):

    firmware_dict = {
            'img-version': f'{aos_compliance_version}',
            'mac-addr': f'{mac_addr}',
            'imagehost': f'{scp_server}',
            'username': f'{scp_user}',
            'image-path': '.',
            'passwd': f'{scp_password}'
        }
    
    firmware_json = json.loads(firmware_dict)

    session.post('configuration/object/upgrade_lcs_copy_scp_reboot', firmware_json, f'/md/cma/shops/{mac_addr}')

def get_new_device():

    #Check MM node hierarchy for devices that have not been renamed, yet.
    node_hierarchy = session.get('configuration/object/node_hierarchy')

    #Define data from nested JSON that is retrieved (needs modification depending on hierarchy structure)
    ctrl_json = node_hierarchy['childnodes'][1]['childnodes'][0]['childnodes'][0]['devices']

    ctrl_list = list() #create list to append multiple new controllers

    isDefault = False
    
    #Check each entry in JSON if it starts with 'CTRL_' and append to list if True
    for md in ctrl_json:
        currHostname = md['name']

        if 'CTRL_' in currHostname:
            isDefault = True
            print('New device detected: ' + currHostname) 

            mac_addr = md['mac']
            ctrl_list.append(mac_addr)

        else:
            pass

    if isDefault == False:
        print('No new devices found.')

    #Return list of new controllers    
    return ctrl_list, isDefault

def get_uplink_ip(mac_addr):

    #Fetch IPSEC map of specified controller through 'show command' API
    cli_json = session.cli_command(f'show crypto-local ipsec-map tag default-local-master-ipsecmap-{mac_addr}-link1')

    #Iterate through JSON text to find the line with starts with 'Destination network' using regex
    for line in cli_json['_data']:

        m = re.match('^Destination network:', line)

        if  m is not None:

            #Remove text from string, except IP/Netmask combination, eg. 10.110.224.23/255.255.255.255. 
            # Variable is NOT modified!
            sub_string = re.sub("Destination network: ", "", line)
            print (re.sub("Destination network: ", "", line))

            uplink_ip = ipaddress._split_optional_netmask(sub_string)
            
            uplink_ip = uplink_ip[0]

            break
    
    #Return uplink VLAN IP 
    return uplink_ip

def get_uplink_nwaddr(uplink_ip):

    #fetch network address of uplink_ip
    iface = ipaddress.ip_interface(f'{uplink_ip}/28')
    nwaddr = iface.network.network_address
    print (nwaddr)

    return nwaddr

def get_shop_details():

    #variable definition
    csv_filename = 'cma-shop-list-unix.txt'
    cwd = os.getcwd()
    
    #Display current working directory
    print ('Current Working Directory is: ' + cwd)

    #Open CSV in read-only mode
    csv_file = open(csv_filename, 'r', encoding='utf8')
    reader = csv.reader(csv_file)

    #Create empty dictionary
    shop_details = {}

    #Headers in CSV: network-address,sap-id,street,zip,place,state
    #Read all lines in CSV and put them in the dictionary. Return dictionary
   
    for row in reader:
        shop_details[row[0]] = {'sap-id':row[1], 'street':row[2], 'zip':row[3], 'place':row[4], 'state':row[5]}

    return shop_details

def set_hostname(new_hostname, mac_addr):

    new_hostname_json = { "hostname": f"{new_hostname}" }
    
    curr_hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = curr_hostname_json['_data']['hostname']['hostname']

    print('Controller ' + curr_hostname + ' will now be renamed to ' + new_hostname)
    time.sleep(3)

    session.post('configuration/object/hostname', new_hostname_json, f'/md/cma/shops/{mac_addr}')
    print('New hostname configured, saving configuration and waiting for sync...')
    
    session.write_memory(f'/md/cma/shops/{mac_addr}') 

    time.sleep(10)
    hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = hostname_json['_data']['hostname']['hostname']

    print ('Controller successfully renamed to ' + curr_hostname)

#Instantiate API session variable
session = api_session(vmm_hostname, admin_user, admin_password, check_ssl=False)

#Set AOS firmware upgrade variables

aos_compliance_version = '8.4.0.0_68230'
scp_server = '192.168.230.23'
scp_user = 'admin'
scp_password = 'Aruba1234'

#Import Shop CSV into dictionary for further processing
print ('Reading shop list...')
time.sleep(2)
shop_dict = get_shop_details()

#Login to MM
print('Login to Mobility Master...')
session.login()

#Fetch new controllers
print ('Check for new controllers...')
time.sleep(2)
new_ctrl, isDefault = get_new_device()

#If there are no controllers matching 'CTRL_' in the hostname, exit the application.
if isDefault is False:
    print ('Closing application.')
    quit()
else:
    pass

#If there are new controllers detected proceed with initial configuration. Exceptions lead to termination of this section.
try:
    #Iterate through list of new controllers.
    for md in new_ctrl:
        ctrl_mac = md
        uplink_ip_list = list()

        #Fetch uplink IP from IPSEC SA information
        print (f'Fetching controller uplink IP for {ctrl_mac} now...')
            
        uplink_ip = get_uplink_ip(md)
        uplink_ip_list.append(uplink_ip)

        #Get uplink IP network address 
        nwaddr = str(get_uplink_nwaddr(uplink_ip))   

        #Configure new hostname
        new_hostname = shop_dict[nwaddr]['sap-id'] +'-'+ shop_dict[nwaddr]['place'] + '-' + shop_dict[nwaddr]['state']
        print('The new controller name is: ' + new_hostname)
        print('The controller MAC address is: ' + ctrl_mac)
        print('Now configuring new hostname, please wait...')
        time.sleep(3)

        set_hostname(new_hostname, ctrl_mac)

        #Fetch upgrade status and MD firmware details
        upgrade_status = session.cli_command(f'show upgrade managed-devices status summary single {ctrl_mac}')
        md_firmware_details = upgrade_status['upgrade managed-node status summary'][0]
        md_firmware_version = md_firmware_details['Current Ver']

        print(md_firmware_version)


        if md_firmware_version != aos_compliance_version:

            print('Attemptting firmware upgrade to ' + aos_compliance_version)
            time.sleep(3)

            firmware_upgrade(ctrl_mac, aos_compliance_version, scp_server, scp_user, scp_password) 

            print('Upgrade initiated waiting 20s for upgrade to be initiated...')
            time.sleep(20)
            md_upgrade_status = session.cli_command(f'show upgrade managed-devices status summary single {ctrl_mac}')
            print(md_upgrade_status)
    
        else:
            print('Controller ' + new_hostname + 'is already on compliance version ' + aos_compliance_version)
            print('Skpping firmware upgrade.')
       
except:
    print(sys.exc_info())
    print ('IP address information not found in shop list or unknown exception raised. Please configure controller manually.')

#print ('List of uplink IPs:')
#print (uplink_ip_list)

#Terminate MM session
session.logout()