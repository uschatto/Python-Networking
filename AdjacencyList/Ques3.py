#!/usr/bin/python

import paramiko
import time
import sys
import json

print("Usage : python <script.py> <No. of devices> <IP addresses>")
IP1 = "1.1.1.2"
IP2 = "1.1.1.3"
IP3 = "1.1.1.4"
print ("SAMPLE INPUT : python Ques3.py 3 '[\"") + IP1 + ("\",\"") + IP2 + ("\",\"") + IP3 + ("\"]'")
print '\n'
number = sys.argv[1]
username = "exam"
password = "exam"
data = json.loads(sys.argv[2])
i = 1
global_network_devices = {}
for ip_address in data:
    #Making a ssh connection
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_address,username=username,password=password)
    #CISCO CLI commands to extract the required information
    remote_connection = ssh_client.invoke_shell()
    remote_connection.send("en\n")
    remote_connection.send("en\n")
    remote_connection.send("conf t\n")
    remote_connection.send(" do sh version\n")
    time.sleep(0.5)
    remote_connection.send("               \n")
    remote_connection.send(" do sh cdp neighbors detail\n")
    time.sleep(0.5)
    remote_connection.send("               \n")
    time.sleep(1)
    output = remote_connection.recv(65535)
    with open('%s.txt'%ip_address, 'w') as f:
         print >>f,output
    f.close()
    fileoutput = open("%s.txt"%ip_address,'r')
    for line in fileoutput:
        line = line.rstrip('\r\n')
        if 'uptime ' in line:
            Localhostname = line.split()[0]
            print Localhostname + '(node)->'
        global_network_devices['Local_hostname'] = {}
        if 'Device ID: ' in line: 
            (junk,hostname) = line.split('Device ID: ')
            hostname = hostname.strip()
            global_network_devices['Local_hostname']['Adjacent Host Name']=hostname
        if 'Interface: ' in line:
            (junk,LocalInterface) = line.split('Interface: ')
            LocalInterface = LocalInterface.split(',')[0]
            global_network_devices['Local_hostname']['Local Node Interface']= LocalInterface
            remote_connection.send("  do sh int " + LocalInterface + " switchport\n")
            time.sleep(1)
            oo = remote_connection.recv(65535)
            with open("%dvlan.txt"%i,'w') as f1:
                 print >>f1, oo
            f1.close()
            fo = open("%dvlan.txt"%i,'r')
            oo = fo.readlines()
            fo.close()
            for l in oo:
                l = l.rstrip('\r\n')
                if l.startswith("Operational Mode: trunk"):
                    for ll in oo:
                        ll = ll.rstrip('\r\n')
                        if 'Trunking VLANs Enabled: ' in ll:
                            (junk,trunkport) = ll.split('Trunking VLANs Enabled: ')
                            trunkport = trunkport.strip()
                            global_network_devices['Local_hostname']['Local VLAN']= trunkport
                            global_network_devices['Local_hostname']['Adjacent Neighbor VLAN'] = trunkport
                elif l.startswith("Operational Mode: static access"):
                    for ll in oo:
                        ll = ll.rstrip('\r\n')
                        if 'Access Mode VLAN: ' in ll:
                            (junk,accessport) = ll.split('Access Mode VLAN: ')
                            accessport = accessport.strip()
                            global_network_devices['Local_hostname']['Local VLAN']= accessport
                            global_network_devices['Local_hostname']['Adjacent Neighbor VLAN']=accessport

            i = i + 1
        if '(outgoing port): ' in line:
            (junk,NeighborInterface) = line.split('(outgoing port): ')
            NeighborInterface = NeighborInterface.strip()
            global_network_devices['Local_hostname']['Adjacent Neighbor Interface']= NeighborInterface
        for data in global_network_devices:
            for line in global_network_devices[data]:
                print '          ' + line + ' : ' + global_network_devices[data][line]
                if (line == "Adjacent Neighbor VLAN"):
                    print '\n'
                    
    ssh_client.close()
