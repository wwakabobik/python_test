import io
import sys
import string
import socket
import os
import re
import fnmatch
from os import listdir
from os.path import isfile, join

# globals, maybe it's better use params instead them
IPAddr = "0.0.0.0"       # IP address
fileMask = "*.log"    # file mask
numPattern = "1900-1-1"   # number pattern
fileName = ""     # full filename

# HARDCODE - I don't know details, therefore let it be so
pathToServerFileFolder = "data/folder"
portNo = "1024"

########################### Functions downhere ################################

# check that the IP is valid
def checkIPAddrExistance(IPAddr):
    try:
        socket.inet_aton(IPAddr)
        #connectToServer(auth_data(IPAddr))    #UNCOMMENT BEFORECOMMIT
    except socket.error:
        print("IP Address not valid, aborting!")
        sys.exit("-1")
    return

# check if file exists, abort if none /straight method/
def checkFileExistance(fileMask):
    global fileName
    fileName = "\\" + IPAddr + "/" + pathToServerFileFolder + "/" + fileMask
    #fileName = pathToServerFileFolder + "/" + fileMask
    if not os.path.exists(fileName):
        print("file not found, abort!")
        sys.exit("-1")
    return (fileName)

# check if file exists, abort if none /re method, local/    
def checkFileExistanceReLoc(fileMask):
    global fileName
    fileName = "\\" + IPAddr + "/" + pathToServerFileFolder + "/*" + fileMask + "*"
    #fileName = pathToServerFileFolder + "/*" + fileMask + "*"
    mypath = "\\" + IPAddr + "/" + pathToServerFileFolder
    #mypath = pathToServerFileFolder
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    findFiles = []
    parrent = re.compile("|".join(map(fnmatch.translate, fileName)), re.I).match
    #for filename in filter(parrent, onlyfiles):
    #    print(filename)
    d = {filename: (onlyfiles) for filename in filter(parrent, onlyfiles)}
    if not d:
        print("file not found, abort!")
        sys.exit("-1")
    else:
        findFiles.append(max(d, key=lambda i: d[i]))
    if not findFiles:
        print("file not found, abort!")
        sys.exit("-1")
    fileName = "\\" + IPAddr + " / " + pathToServerFileFolder + "/" + findFiles[0]
    #fileName = pathToServerFileFolder + "/" + findFiles[0]
    return (fileName) # return first match, don't care about others

# check if file exists, abort if none /re method, ftp/    
def checkFileExistanceReFTP(fileMask):
    global fileName
    fileName = "\\" + IPAddr + "/" + pathToServerFileFolder + "/*" + fileMask + "*"
    #fileName = pathToServerFileFolder + "/*" + fileMask + "*"
    findFiles = []
    parrent = re.compile("|".join(map(fnmatch.translate, fileName)), re.I).match
    d = {filename: ((ftp.sendcmd('MDTM ' + filename))[4:]) for filename in filter(parrent, onlyfiles)}
    if not d:
        print("file not found, abort!")
        sys.exit("-1")
    else:
        findFiles.append(max(d, key=lambda i: d[i]))
    if not findFiles:
        print("file not found, abort!")
        sys.exit("-1")
    fileName = "\\" + IPAddr + " / " + pathToServerFileFolder + "/" + findFiles[0]
    #fileName = pathToServerFileFolder + "/" + findFiles[0]
    return (fileName) # return first match, don't care about others
    
# connect to server using login/password
def connectToServer(login, password):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((IPAddr, portNo))
    clientsocket.send(login)
    #print(clientsocket.recv(1024)) # commented-out to supress debug output
    clientsocket.send(password)
    #print(clientsocket.recv(1024)) # commented-out to supress debug output
    return
    
# get user input
def userInput():
    global numPattern
    print("Enter IP addres of server: ")
    IPAddr = input()
    checkIPAddrExistance(IPAddr)
    print("Enter file mask: ")
    fileMask = input()
    # Using local method 
    fileName = checkFileExistanceReLoc(fileMask)
    # Comment-out FTP method
    #fileName = checkFileExistanceReLoc(fileMask)
    print("Enter num ID: ")
    numPattern = int(input())
    return

# find number of first line with pattern match, return -1 if not found
def findFirstMatch():
    counter = 0
    # we're using utf-8 encoding, but can be changed to any
    global numPattern
    with io.open(fileName, encoding='utf-8') as file:
        for line in file:
            counter += 1
            if str(numPattern) in line:
                file.close()
                return counter
                break
    file.close()
    return -1
    
# print area
def printArea(lineStart, lineEnd):
    # we don't care if lineStart or lineEnd will be out of bounds
    # because these conditions is not reachable by our loop
    lines=[i for i in range(lineStart,lineEnd)]
    i = 0
    f = open(fileName)
    for line in f:
        if i in lines:
            print(line, end=' ')
        i += 1
    return

# calling function
def findLogs():
    userInput()
    firstMatchLine=findFirstMatch()
    if firstMatchLine == -1:
        print("Pattern not found in file!")
    else:        
        printArea(firstMatchLine - 100, firstMatchLine + 100)
    return
        
###############################################################################

# run script

# start 
findLogs()
