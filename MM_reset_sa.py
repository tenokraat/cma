import paramiko
import cmd
import time
import sys

buff = ''
resp = ''

f = open ('/home/aruba/environments/cma/reset-logs/srvma230-024-reset-log.txt', 'a+')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.230.23', username='python', password='Aruba1234')
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
chan = ssh.invoke_shell()

# turn off paging
chan.send('terminal length 0\n')
time.sleep(1)
resp = chan.recv(9999)
output = resp.decode('ascii').split(',')
#print (''.join(output))

# Display output of first command
chan.send('show clock')
chan.send('\n')
time.sleep(1)
resp = chan.recv(9999)
output = resp.decode('ascii').split(',')
f.write (''.join(output))

# Display output of second command
chan.send('clear crypto isakmp sa')
chan.send('\n')
time.sleep(1)
resp = chan.recv(9999)
output = resp.decode('ascii').split(',')
f.write (''.join(output))

# Display output of third command
chan.send('clear crypto ipsec sa')
chan.send('\n')
time.sleep(1)
resp = chan.recv(9999)
output = resp.decode('ascii').split(',')
f.write (''.join(output))

f.close()

ssh.close()  
