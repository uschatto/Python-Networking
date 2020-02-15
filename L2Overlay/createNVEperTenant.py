#!/usr/bin/python
import paramiko
import time
import os

print "Assuming the underlay topology is intact, we will proceed towards creation of the overlay network for the 3 tenants"
print "########## Naming Conventions ##########"
print "The name of spine switches are : S1, S2 (fixed for this script)"
print "The name of leaf switches are: L1, L2, L3 (will be picked from the TenantInput.txt file's first column"
print "The name of tenant servers are: T1H1, T1H2, T2H3, T2H4, T1H5, T1H6, T3H7, T3H8, T2H9, T2H10, T3H11, T3H12 (will be picked from the TenantInput.txt file's 2nd and 3rd columns)"
print "Tenant bridges : T1br, T2br and T3br"

pre_requisite="apt-get install bridge-utils"
interface_ip="192.168."

interface_name="eth"
#Logic for getting the management IP addresses of the machines on which we need to configure the tenant bridges and overlay network
management_ip_dict={}
f=open("/home/ece792/RND-TOOL/rnd_lab/scripts/connectivitymat.txt","r")
lines=f.readlines()
i = 2
management_ip = "172.17.0."
for x in lines:
    server = x.split(' ',1)[0]
    if server:
       management_ip_dict[server] = management_ip+str(i)
       i+=1
f.close()

#Logic for getting the Leaf names and the names of the Tenant hosts connected to them
host_details={}
vxlan={}
with open ("TenantInput.txt") as file:
        for line in file:
                data=line.split('}')[:-1]
                leaf_name=data[0][1:]
                host_details[leaf_name]={}
                for i in range(1,len(data)):
                        tenant_data=data[i].split('{')
                        tenant_id=tenant_data[0].split(',')[1]
			vxlan[tenant_id]=vxlan.get(tenant_id,int(tenant_id[-1]))
                        host_servers=tenant_data[1].split(',')
                        host_details[leaf_name][tenant_id]=[]
                        for j in host_servers:
                                host_details[leaf_name][tenant_id].append(tenant_id+j)
for leaf,tenant_servers in host_details.items():
     leaf_id=leaf[-1]
     initial_command = "sudo docker exec " + leaf + " " + pre_requisite
     os.system(initial_command)
     print "Executing virtualisation operations on leaf switch : " + leaf
     for tenant_id,server_name in tenant_servers.items():
         i += 1
         print "Creating tenant bridge for : " + tenant_id
         interface_ids={}
         interface_ips={}
         cmdlist=[]
	     interface_ids[tenant_id]=[]
         interface_ips[tenant_id]=[]
         
         #Logic for getting the interface names in leaf switches to which the tenant servers are connected
         for server in server_name:
             interface_ids[tenant_id].append(interface_name+str(int(management_ip_dict[server].split('.')[3])-1)+"1")
             interface_ips[tenant_id].append(interface_ip + str(int(management_ip_dict[server].split('.')[3])) + ".1")
         cmdlist.append("sudo docker exec " + leaf+ " brctl addbr "+ tenant_id + "br")
         cmdlist.append("sudo docker exec " + leaf+ " ip link set dev " + tenant_id + "br up")
         for ip,idd in zip(interface_ips[tenant_id],interface_ids[tenant_id]):
             cmdlist.append("sudo docker exec " + leaf+ " ip addr del " + ip + "/24 dev " + idd)
             cmdlist.append("sudo docker exec " + leaf+ " brctl addif " + tenant_id + "br " + idd)
         cmdlist.append("sudo docker exec " + leaf+ " ip link add vxlan" + str(vxlan[tenant_id]*100) + " type vxlan id " + str(vxlan[tenant_id]*100) + " dstport 4789 local " + leaf_id + "." + leaf_id + "." + leaf_id + "." + leaf_id)
         cmdlist.append("sudo docker exec " + leaf + " ip link set dev vxlan" + str(vxlan[tenant_id]*100) + " up")
         cmdlist.append("sudo docker exec " + leaf + " brctl addif " + tenant_id + "br vxlan" + str(vxlan[tenant_id]*100))
         for cmd in cmdlist:
             os.system(cmd)
