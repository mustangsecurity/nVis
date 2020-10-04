#!/usr/bin/python3
import os
from ftplib import FTP
import ftplib

# CONFIGURE FTP FOR NVIS MASTER SERVER
print("[+] Configuring FTP options for master server")
print("**********************************************")
username = 'anonymous'
remote_path = "pub"
remoteIP = input("Enter Remote FTP Server IP: ")
nmapdb = input("Enter your name: ")
subnet =input("Enter IP Address/CIDR for scan: ")
server = remoteIP

# ATTEMPT TO INSTALL NMAP IF NOT ALREADY PRESENT
print()
print("[+] Attempting to install nmap")
print("******************************")
os.system("apt-get install nmap -y")

# CONFIGURE NMAP SCANS
first = "nmap -n -sn " + subnet + " -oG - | awk '/Up$/{print $2}' > first.txt"
second = "nmap -v -T5 " + subnet + " -p21,22,23,25,110,139,443,445,3000,3389,8080 | grep Discovered | awk '{print $6}' > second.txt"

# RUN THE PING SCAN to DISCOVER PINGABLE HOSTS
print("[+] Running ping sweep of " + subnet)
print("***********************************")
os.system(first)
print("[+] Discovered hosts:")
os.system("cat first.txt")

# RUN A SCAN OF COMMON PORTS TO DISCOVER ANY HOSTS THAT DON'T LISTEN TO ICMP (WINDOWS)
print("[+] Running port-based host discovery on " + subnet)
print("*********************************************************")
os.system(second)
os.system("sort first.txt second.txt | uniq > hostlist.txt")
print("[+] Final list of discovered hosts: ")
os.system("cat hostlist.txt")

# CONDUCT THE PORT SCAN
print("[+] Conducting a port scan of top TCP ports.")
print("**************************************************")
print("note: ensure to still conduct further recon of high ports and UDP")

os.system("nmap -sS -sV -T5 -iL hostlist.txt -oA " + nmapdb)
print("Scan completed!")

# UPLOAD THE RESULTS
print("[+] Uploading results to master server")
print("*******************************************")
print("[+] Connecting to master FTP server")
ftp_connection = ftplib.FTP(server, username)

print("[+] Entering the pub directory")
ftp_connection.cwd(remote_path)

print("[+] Disabling passive mode")
ftp_connection.set_pasv(True)

print("[+] Uploading file via binary")
fh = open(nmapdb +".xml" , 'rb')
ftp_connection.storbinary("STOR %s.xml" % nmapdb, fh)
fh.close()

print("[+] Closing FTP connection")
ftp_connection.quit()
	
print("[+] Have a nice day :)")
	
	
