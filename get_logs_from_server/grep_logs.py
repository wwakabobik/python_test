import io
import sys
import socket


# globals, maybe it's better use params instead them
String IPAddr       # IP address
String fileMask     # file mask
String numPattern   # number pattern
String fileName     # full filename

# HARDCODE - I don't know details, therefore let it be so
pathToServerFileFolder = "data/folder"
portNo = "1024"

# start 
findLogs()

########################### Functions downhere ################################

# check that the IP is valid
def checkIPAddrExistance(IPAddr)
    try:
        socket.inet_aton(addr)
        connectToServer(auth_data(IPAddr))    
    except socket.error:
        print("IP Address not valid, aborting!"
		sys.exit(-1)

# check if file exists, abort if none
def checkFileExistance(IPAddr + " / "PathToServerFileFolder + "/" + fileMask)#
	if not os.path.exists(fileMask):
		print("file not found, abort!")
		sys.exit(-1)
	return String(PathToServerFileFolder + "/" + fileMask)
	
# connect to server using login/password
def connectToServer(login, password)
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((IPAddr, portNo))
    clientsocket.send(login)
    #print(clientsocket.recv(1024)) # commented-out to supress debug output
    clientsocket.send(password)
    #print(clientsocket.recv(1024)) # commented-out to supress debug output

# get user input
def userInput()
    print("Enter IP addres of server: ")
    IPAddr = string(input())
	checkIPAddrExistance(IPAddr)
    print("Enter file mask: ")
    fileMask = string(input())
	checkFileExistance(fileMask)
    print("Enter num ID: ")
    numPattern = int(input())
	return

# find number of first line with pattern match, return -1 if not found
def findFirstMatch()
    counter = 0
	found = false
	# we're using utf-8 encoding, but can be changed to any
    with io.open(fileName, encoding='utf-8') as file:
        for line in file:
		    counter += 1
            if numPattern in line:
                io.close()
				return counter
				break
    io.close()
	return -1
	
# print area
def printArea(lineStart, lineEnd)
	# we don't care if lineStart or lineEnd will be out of bounds
	# because these conditions is not reachable by our loop
	lines=[lineStart, lineEnd]
    i = 0
    f = open('filename')
    for line in f:
        if i in lines:
            print i
        i += 1

# calling function
def findLogs()
    userInput()
	firstMatchLine=findFirstMatch()
	printArea(firstMatchLine - 100, firstMatchLine + 100)
