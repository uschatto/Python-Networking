#!/usr/bin/python

import sys
import paramiko

if len(sys.argv) < 4:
     print("Usage : python <script.py> <IP> <username> <password>")
     exit()
else:
     ip = sys.argv[1]
     user = sys.argv[2]
     passwd = sys.argv[3]

print "User wishes to see the details of the host with IP address %s" %ip

while 1: 
	user_input = raw_input('Enter your choice IP? MAC? TYPE? .. Press Quit to exit')
	if (user_input.lower() == "ip"):
    		#Establishing a SSH Connection
    		sshconnection = paramiko.SSHClient()
    		sshconnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    		sshconnection.connect(hostname=ip,username=user,password=passwd)
    		#Command to get the Interface names from "ip a" command
    		stdin,stdout,stderr = sshconnection.exec_command("/sbin/ip a | grep 'mtu' | awk '{print $2}' | cut -d':' -f1")

    		outInterface = stdout.readlines()
    		ArrayInterface ={}
    		for i in range(len(outInterface)):
        		ArrayInterface[i] = outInterface[i].rstrip('\n').encode("utf-8")

    		#Command to get the IP addresses from "ip a" command
    		stdin,stdout,stderr = sshconnection.exec_command("/sbin/ip a | grep -w 'inet' | awk '{print $2}'")
    
    		outIPAddress = stdout.readlines()
    		ArrayIPAddress={}
    		for i in range(len(outIPAddress)):
        		ArrayIPAddress[i] = outIPAddress[i].rstrip('\n').encode("utf-8")
    
    		#Final print to display in proper output 
    		for i in range(len(ArrayInterface)):
        		print "{}) Interface Name [{}] - IP Address [{}]".format(i+1,ArrayInterface[i] ,ArrayIPAddress[i])

	elif (user_input.lower() == "mac"):
      	        #Establishing a SSH Connection
      		sshconnection = paramiko.SSHClient()
      		sshconnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      		sshconnection.connect(hostname=ip,username=user,password=passwd)
      		#Command to get the Interface names from "ip a" command
      		stdin,stdout,stderr = sshconnection.exec_command("/sbin/ip a | grep 'mtu' | awk '{print $2}' | cut -d':' -f1")

      		outInterface = stdout.readlines()
      		ArrayInterface ={}
      		for i in range(len(outInterface)):
          		ArrayInterface[i] = outInterface[i].rstrip('\n').encode("utf-8")

      		#Command to get the MAC addresses from "ip a" command
      		stdin,stdout,stderr = sshconnection.exec_command("/sbin/ip a | grep 'link' | grep -v 'scope' | awk '{print $2}'")

      		outMACAddress = stdout.readlines()
      		ArrayMACAddress={}
      		for i in range(len(outMACAddress)):
          		ArrayMACAddress[i] = outMACAddress[i].rstrip('\n').encode("utf-8")

      		#Final print to display in proper output
      		for i in range(len(ArrayInterface)):
          		print "{}) Interface Name [{}] - MAC Address [{}]".format(i+1,ArrayInterface[i] ,ArrayMACAddress[i])    
 
	elif (user_input.lower() == "type"):
      		#Establishing a SSH Connection
      		sshconnection = paramiko.SSHClient()
      		sshconnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      		sshconnection.connect(hostname=ip,username=user,password=passwd)
      		#Command to get the Interface names from "ip a" command
      		stdin,stdout,stderr = sshconnection.exec_command("/sbin/ip a | grep 'mtu' | awk '{print $2}' | cut -d':' -f1")

      		outInterface = stdout.readlines()
      		ArrayInterface ={}
      		for i in range(len(outInterface)):
          		ArrayInterface[i] = outInterface[i].rstrip('\n').encode("utf-8")

      		#Command to get the Interface Types from "ip a" command      
      		stdin,stdout,stderr = sshconnection.exec_command("/sbin/ip a | grep 'link' | grep -v 'scope' | awk '{print $1}' | cut -d'/' -f2")
      
      		outType = stdout.readlines()
      		ArrayType ={}
      		for i in range(len(outType)):
          		ArrayType[i] = outType[i].rstrip('\n').encode("utf-8")

      		#Final print to display in proper output
      		for i in range(len(ArrayInterface)):
          		print "{}) Interface Name [{}] - Interface Type [{}]".format(i+1,ArrayInterface[i] ,ArrayType[i])
        elif (user_input.lower() == "quit"):
        	print "User wishes to quit"
                exit()
	else : 
      		print "Please enter a correct choice"
