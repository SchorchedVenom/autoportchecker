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
import array as arr

#Variables
global fileOutputFile
global portNumbers
global ipAddressCount
global ipAddress
global configFile
global diffOutputFile

#Config Creation
configFile = open("config.txt", "w")

#User Interaction
os.system('clear')
print("Welcome to the 1 time configuration script!")
fileOutputFile = input("Please enter the desired name for your output file: ")
print("fileOutput={}".format(fileOutputFile),file=configFile)
diffOutputFile = input("Please enter the desired name for you diff output file: ")
print("diffOutput={}".format(diffOutputFile),file=configFile)
os.system('clear')
x = 0
portArray = arr.array('i')
while x == 0:
    response = input("Which Port Numbers Would You Like To Scan?\n1.1-1023 \n2.1-65535 \n3.Enter your own port numbers \nPlease Choose one of the above: ")
    if response == "1":
        port = 1
        while port < 1024:
            portArray.append(int(port))
            port += 1
        portList = portArray.tolist()
        print("portNumbers={}".format(portList),file=configFile)
        x = 1
    elif response == "2":
        port = 1
        while port < 65536:
            portArray.append(int(port))
            port += 1
        portList = portArray.tolist()
        print("portNumbers={}".format(portList),file=configFile)
        x = 1
    elif response == "3":
        os.system('clear')
        port = ""
        while port != "exit" or port != "Exit":
            os.system('clear')
            port = input("Please enter a port to scan or enter Exit to finish: ")
            if port != "exit" or port != "Exit":
                portArray.append(int(port))
            else:
                portList = portArray.tolist()
                print("portNumbers={}".format(portList),file=configFile)
                x = 1
    else:
        os.system('clear')
        input("Invalid response, press enter to try again!")

#Ip Address Count
os.system('clear')
ipArray = arr.array('i')
print("Would you like to scan more than 1 IP Address?")
x = 0
response = input("1.Yes\n2.No")
while x == 0:
    if response == "1" or response == "yes" or response == "Yes":
        ipAddress = ""
        print("ipAddressCount=Yes")
        while ipAddress != "exit" or ipAddress != "Exit":
            os.system('clear')
            ipAddress = input("Please enter a IP to scan or enter Exit to finish: ")
            if ipAddress != "exit" or ipAddress != "Exit":
                ipArray.append(int(ipAddress))
            else:
                ipList = ipArray.tolist()
                ipFile = open("ipaddress.txt", "w")
                print("ipAddress={}".format(ipList),file=ipFile)
                x = 1
                ipFile.close()
    elif response == "2" or response == "no" or response == "No":
        ipAddress = input("Please enter your target IP Address: ")
        print("ipAddress={}".format(ipAddress),file=configFile)
        x = 1
    else:
        input("Invalid Response! Please press enter to try again!")

configFile.close()

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

#Create Initial scan file
outPutTransfer = [line.rstrip('\n') for line in open("./{}".format(fileOutputFile))]
initOutput = open("init_scan.txt", "w")
for line in outPutTransfer:
    print("{}".format(i),file=ininitOutput)
initOutput.close()

#Create Cronfile
currentDirectory = os.getcwd()
pythonCommand = "@hourly python3 " + str(currentDirectory) + "/PortChecker.py"
cronCommand = "crontab " + str(currentDirectory) + "/PortCheckerCron"
cronFile = open("PortCheckerCron", "w")
print("{}".format(pythonCommand),file=cronFile)
cronFile.close()
os.system(str(cronCommand))
