#!/usr/bin/env python3
import json
from fmcapi import *
import getpass
import csv
from tkinter import filedialog
from tkinter import *

############# Settings
autodeploy = False

# Get information
fmchost =   input("FMC Server: ")
username =  input("Username: ")
password =  getpass.getpass(prompt='Password: ')
#filename = input("Enter Filename:") 


root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select CSV file to import",filetypes = (("CSV","*.CSV"),("All Files","*.*")))
filename = str(root.filename)

 
with open(filename, encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    with FMC(host=fmchost, username=username, password=password, autodeploy=autodeploy) as fmc1:
        for row in reader:
                        
                        # Build strings for creating object
                        ip = (ipaddress.ip_interface(str(row['ip'])))
                        firewall = (str(row['firewall']))
                        interface = (str(row['interface']))
                        ipversion = (str(ip.version))

                        # Build object & Post
                        objname = "obj" + ipversion + "-" + firewall + "-" + interface
                        objdesc = "Interface " + interface + " on " + firewall

                        # Check for host prefix
                        if (ip.network.prefixlen == 32 and ip.version == 4) or (ip.network.prefixlen == 128 and ip.version == 6):
                            obj1 = IPHost(fmc=fmc1)
                            obj1.value = str(ip.compressed)
                        else:
                            obj1 = IPNetwork(fmc=fmc1)
                            obj1.value = str(ip.network.compressed)
                            pass

                        obj1.name = objname
                        obj1.description = objdesc
                        obj1.post()
                        del obj1
                        
                        print("Complete")
