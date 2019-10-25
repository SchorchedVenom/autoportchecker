#SchorchedVenom
#10/24/2019
#
#Based on Reddit request on r/AskNetsec
#
#!/usr/bin/python3
#
#Libraries
import os
import subprocess
import socket
import difflib

#Variables
global fileOutputFile
global portNumbers
global ipAddressCount
global ipAddress
global configFile
global diffOutputFile

#Config Import
configFile = [line.rstrip('\n') for line in open("./config.txt")]

#Variable Extraction
x = 0
for i in configFile:
    if x == 0:
        fileOutputFile = i.rstrip('fileOutput=')
        x += 1
    elif x == 1:
        diffOutputFile = i.rstrip('diffOutput=')
        x += 1
    elif x == 2:
        portNumbers = i.rstrip('portNumbers=')
        x += 1
    elif x == 3:
        ipAddressCount = i.rstrip('ipAddressCount=')
        if ipAddressCount == "Yes":
            ipAddress = [line.rstrip('\n') for line in open("./ipaddress.txt")]
            x = 5
        else:
            x += 1
    elif x == 4:
        ipAddress = i.rstrip('ipAddress=')
    elif x == 5:
        pass
    
#Setup Output File
outPutTransfer = [line.rstrip('\n') for line in open("./{}".format(fileOutputFile))]
previousOutput = open("./previous_output.txt", "w")
for i in outPutTransfer:
    print("{}".format(i),file=previousOutput)
previousOutput.close()
fileOutput = open(fileOutputFile,"w")

#Run Port Map
socket.setdefaulttimeout(10)
for i in ipAddress:
    print ("------{}------".format(i),file=fileOutput)
    targetServer = socket.gethostbyname(i)
    for port in portNumbers:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        result = sock.connect_ex((targetServer,port))
        if result == 0:
            print("Port:{}    Open".format(port),file=fileOutput)
            sock.close()
            banner = ""
            if port == 80 or port == 8080 or port == 443 or port == 4434:
                sock = socket.socket()
                sock.connect((targetServer,port))
                sock.send(b'HEAD /\n\n')
                banner = sock.recv(1024)
            else:
                sock = socket.socket()
                sock.connect((targetServer,port))
                banner = sock.recv(1024)
            print("Port:{}  ".format(port) + "Banner:{} ".format(banner),file=fileOutput)
            sock.close()
fileOutput.close()

#Difference Checking Start
diffOutput = open(diffOutputFile,"w")

#Init Difference Check
print("------Initial Scan Difference------",file=diffOutput)
initOutput = [line.rstrip('\n') for line in open("./{}".format("./init_scan.txt"))]
fileOutput = [line.rstrip('\n') for line in open("./{}".format(fileOutputFile))]
for line1, line2 in zip(initOutput, fileOutput):
    diff = difflib.unified_diff(text1_lines, text2_lines, lineterm='')
    print("{}".format(diff),file=diffOutput)

#Previous Difference Check
print("\n------Previous Scan Difference------",file=diffOutput)
previousOutput = [line.rstrip('\n') for line in open("./{}".format("./previous_output.txt"))]
fileOutput = [line.rstrip('\n') for line in open("./{}".format(fileOutputFile))]
for line1, line2 in zip(previousOutput, fileOutput):
    diff = difflib.unified_diff(text1_lines, text2_lines, lineterm='')
    print("{}".format(diff),file=diffOutput)
diffOutput.close()