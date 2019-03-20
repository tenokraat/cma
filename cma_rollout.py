#!/usr/bin/python3

import json,requests,re,csv,os,sys,time
import ipaddress
from tomtom_geolocation import *
from aruba_api_caller import *

#logging.basicConfig(level=logging.DEBUG)

#MM Login Credentials ##

vmm_hostname = '192.168.230.23'
admin_user = 'python'
admin_password = 'Aruba1234'

#vmm_hostname = input ('VMM Hostname or IP: ')
#admin_user = input('Enter username: ')
#admin_password = input(f'Enter {admin_user} password: ')

#Set AOS firmware upgrade variables

aos_compliance_version = '8.4.0.0_68230'
scp_server = '192.168.230.23'
scp_user = 'admin'
scp_password = 'Aruba1234'
fw_success = False

def firmware_upgrade(ctrl_mac):

    #Create dictionary with all firmware parameters
    firmware_params = {
            'img-version': aos_compliance_version,
            'mac-addr': ctrl_mac,
            'imagehost': scp_server,
            'username': scp_user,
            'image-path': '.',
            'passwd': scp_password
        }
    
    #Fetch current upgrade status
    print(f'>>> Fetching current upgrade status for {ctrl_mac}')

    if upgrade_status_copy_status['Copy Status'] == 'Download in-progress':
        print(f'>>> Download for {ctrl_mac} still in progress, skipping additional firmware tasks.')
        fw_success = False
        
    elif upgrade_status_copy_status['Copy Status'] == 'Update in-progress':
        print(f'>>> Update for {ctrl_mac} still in progress, skipping additional firmware tasks.')
        fw_success = False
        
    #elif re.match(f'^Successfully updated flash with ArubaOS_70xx_{aos_compliance_version}$', upgrade_status_copy_status['Status Description']) is not None:
    #    print(f'>>> Node {ctrl_mac} has been already successfully updated to {aos_compliance_version}, skipping additional firmware tasks.')
    #    fw_success = False
        
    elif upgrade_status_copy_status['Copy Status'] == 'waiting':
        print(f'>>> Waiting for response from {ctrl_mac}, skipping additional firmware tasks.')
        fw_success = False
        
    else:
           
        time.sleep(2)

        print(f'>>> No existing update in progress, attemptting firmware upgrade to  {aos_compliance_version}')
        time.sleep(2)

        #Execute firmware update
        firmware_json = json.dumps(firmware_params)

        session.post('configuration/object/upgrade_lcs_copy_scp_reboot', json.loads(firmware_json), '/md')

        print('>>> Upgrade initiated waiting for upgrade to be begin...')
        time.sleep(20)
        print(upgrade_status_copy)

        print(f'>>> Skipping controller {ctrl_mac} renaming until next run and firmware upgrade is completed.')

        fw_success = True

    return fw_success
    
def get_new_device():

    #Check MM node hierarchy for devices that have not been renamed, yet.
    node_hierarchy = session.get('configuration/object/node_hierarchy')

    #Define data from nested JSON that is retrieved (needs modification depending on hierarchy structure)
    ctrl_json = node_hierarchy['childnodes'][1]['childnodes'][0]['childnodes'][0]['devices']

    ctrl_list = list() #create list to append  new controller mac addresses

    isDefault = False
    
    #Check each entry in JSON if it starts with 'CTRL_' and append to list if True
    for md in ctrl_json:
        currHostname = md['name']

        if 'CTRL_' in currHostname:
            isDefault = True
            print('>>> New device detected: ' + currHostname) 
            time.sleep(2)

            mac_addr = md['mac']
            ctrl_list.append(mac_addr)

        else:
            pass

    if isDefault == False:
        print('>>> No new devices found. <<<')
        time.sleep(2)

    #Return list of new controllers   
    return ctrl_list, isDefault

def get_md_status(ctrl_mac):

    #Check state of MDs
    all_switches = session.cli_command('show switches debug')
    switchinfo = all_switches['All Switches']

    key = 0

    for each in switchinfo:
        if switchinfo[key]['MAC'] == ctrl_mac:
            md_status = switchinfo[key]['Status']
            break
        else:
            key = key + 1

    return md_status

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
            print ('>>> ' + re.sub("Destination network: ", "", line))

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
    print ('>>> Current Working Directory is: ' + cwd)
    time.sleep(2)

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

    print('>>> Controller ' + curr_hostname + ' will now be renamed to ' + new_hostname)
    time.sleep(3)

    session.post('configuration/object/hostname', new_hostname_json, f'/md/cma/shops/{mac_addr}')
    print('>>> New hostname configured, saving configuration and waiting for sync...')
    
    session.write_memory(f'/md/cma/shops/{mac_addr}') 

    time.sleep(10)
    hostname_json = session.get('configuration/object/hostname', f'/md/cma/shops/{mac_addr}')
    curr_hostname = hostname_json['_data']['hostname']['hostname']

    print ('>>> Controller successfully renamed to ' + curr_hostname)

def set_geolocation(mac_addr, lon, lat):

    geolocation_params = {
        'latitude': lat,
        'longitude': lon
        }

    geolocation_json = json.dumps(geolocation_params)

    print(geolocation_json)

    session.post('configuration/object/geolocation', json.loads(geolocation_json), f'/md/cma/shops/{mac_addr}')

    print ('Geolocation has been set to Longitude: ' + lon + ', Latitude: ' + lat )
    print ('Saving configuration and waiting for sync...')

    session.write_memory(f'/md/cma/shops/{mac_addr}')

    time.sleep(5)

#Instantiate API session variable
session = api_session(vmm_hostname, admin_user, admin_password, check_ssl=False)

#Import Shop CSV into dictionary for further processing
print ('>>> Loading shop list...')
time.sleep(2)
shop_dict = get_shop_details()

#Login to MM
print('>>> Connecting to Mobility Master...')
time.sleep(2)
session.login()

#Fetch new controllers
print ('>>> Checking for new controllers...')
time.sleep(2)
new_ctrl, isDefault = get_new_device()

#If there are no controllers matching 'CTRL_' in the hostname, exit the application.
if isDefault is False:
    print ('>>> Closing application. <<<')
    time.sleep(2)
    quit()
else:
    pass

#If there are new controllers detected proceed with their configuration. Any pyhton exception leads to termination of this section.
try:
    #Iterate through list of new controllers.
    for md in new_ctrl:
        
        ctrl_mac = md
        md_status = get_md_status(ctrl_mac)
        
        print(f'>>> Checking device state, node {ctrl_mac} is {md_status}')

        if md_status == 'up':

            ## Firmware compliance ##

            #Fetch upgrade status and MD firmware details
            upgrade_status_summary = session.cli_command(f'show upgrade managed-devices status summary single {ctrl_mac}')
            md_firmware_details = upgrade_status_summary['upgrade managed-node status summary'][0]
            md_firmware_version = md_firmware_details['Current Ver']
            
            upgrade_status_copy = session.cli_command(f'show upgrade managed-devices status copy single {ctrl_mac}')
            upgrade_status_copy_status = upgrade_status_copy['upgrade managed-node copy command status'][0]
            
            #If controller is on any other release than the configured compliance version, perform upgrade.
            if md_firmware_version != aos_compliance_version:
                fw_success = firmware_upgrade(ctrl_mac)

                if fw_success == True:
                    continue

            elif fw_success == True:
                    continue

            else:
                print(f'>>> Controller {ctrl_mac} is already on compliance version {aos_compliance_version}')
                print('>>> Skpping firmware upgrade.')

            ## Configure new hostname ##
           
            #Fetch uplink IP from IPSEC SA information
            print (f'>>> Fetching controller uplink IP for {ctrl_mac} now... <<<')

            uplink_ip_list = list()    
            uplink_ip = get_uplink_ip(md)
            uplink_ip_list.append(uplink_ip)

            #Get uplink IP network address 
            nwaddr = str(get_uplink_nwaddr(uplink_ip))   
            
            new_hostname = shop_dict[nwaddr]['sap-id'] +'-'+ shop_dict[nwaddr]['place'] + '-' + shop_dict[nwaddr]['state']
            print(f'>>> The new controller name is: {new_hostname}')
            print(f'>>> The controller MAC address is: {ctrl_mac}')
            print('>>> Now configuring new hostname, please wait...')
            time.sleep(3)

            set_hostname(new_hostname, ctrl_mac)

            ## Configure geolocation ##

            #Retrieve shop address from shop list
            shop_address = shop_dict[nwaddr]['street'] +' '+ shop_dict[nwaddr]['zip'] + ' ' + shop_dict[nwaddr]['place']
            print('>>> Fetching location for address: '+ shop_address)

            #Retrieve geolocation data of shop adress
            geoloc = geolocation()
            lat, lon, address = geoloc.get_geolocation(shop_address)
            
            print (f'>>> Retrieved the following geodata information, Longitude:  {lat}, Latitude: {lon}')

            #Configure controller geolocation
            set_geolocation(ctrl_mac, lon, lat)

            print(f'>>> Node {ctrl_mac} configuration fully completed.')
        
        elif md_status == 'down':
            print(f'>>> Node {ctrl_mac} is currently down. Skipping device configuration.')

            continue
                
        else:
            pass
       
except:
    print(sys.exc_info())
    print ('>>> IP address information not found in shop list or unknown exception raised. Please configure controller manually.')

#Terminate MM session
session.logout()