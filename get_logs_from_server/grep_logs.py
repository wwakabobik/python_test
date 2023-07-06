import io
import sys
import socket
import os
import re
import fnmatch
from os import listdir
from os.path import isfile, join

# globals, maybe it's better use params instead them
ip_address = "0.0.0.0"  # IP address
port_no = "21"
file_mask = "*.log"  # file mask
num_pattern = "1900-1-1"  # number pattern
file_name = ""  # full filename

# HARDCODE - I don't know details, therefore let it be so
path_to_server_file_folder = "data/folder"
portNo = "1024"


# Functions bellow


def check_ip_address_existence(ip_address):
    """
    Check that the IP is valid

    :param ip_address: ip address of the ftp server
    :return: None.
    """
    try:
        socket.inet_aton(ip_address)
        # connectToServer(auth_data(ip_address))    #UNCOMMENT BEFORE COMMIT
    except socket.error:
        print("IP Address not valid, aborting!")
        sys.exit("-1")
    return


def check_file_existence(file_mask):
    """
    Check if file exists, abort if none /straight method/

    :param file_mask: filename extension (mask)
    :return: filename (string)
    """
    global file_name
    file_name = "\\" + ip_address + "/" + path_to_server_file_folder + "/" + file_mask
    # file_name = path_to_server_file_folder + "/" + file_mask
    if not os.path.exists(file_name):
        print("file not found, abort!")
        sys.exit("-1")
    return file_name


def check_file_existence_re_loc(file_mask):
    """
    Check if file exists, abort if none /re method, local/

    :param file_mask: filename extension (mask)
    :return: first match of filename using pattern (string)
    """
    global file_name
    file_name = (
        "\\" + ip_address + "/" + path_to_server_file_folder + "/*" + file_mask + "*"
    )
    # file_name = path_to_server_file_folder + "/*" + file_mask + "*"
    mypath = "\\" + ip_address + "/" + path_to_server_file_folder
    # mypath = path_to_server_file_folder
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    find_files = []
    parent = re.compile("|".join(map(fnmatch.translate, file_name)), re.I).match
    # for filename in filter(parent, only_files):
    #     print(filename)
    d = {filename: only_files for filename in filter(parent, only_files)}
    if not d:
        print("file not found, abort!")
        sys.exit("-1")
    else:
        find_files.append(max(d, key=lambda i: d[i]))
    if not find_files:
        print("file not found, abort!")
        sys.exit("-1")
    file_name = (
        "\\" + ip_address + " / " + path_to_server_file_folder + "/" + find_files[0]
    )
    # file_name = path_to_server_file_folder + "/" + find_files[0]
    return file_name


#
def check_file_existence_re_ftp(file_mask):
    """
    Check if file exists, abort if none /re method, ftp/

    :param file_mask: file mask (extension)
    :return: first filename match, don't care about others
    """
    global file_name
    file_name = (
        "\\" + ip_address + "/" + path_to_server_file_folder + "/*" + file_mask + "*"
    )
    # file_name = path_to_server_file_folder + "/*" + file_mask + "*"
    find_files = []
    parent = re.compile("|".join(map(fnmatch.translate, file_name)), re.I).match
    mypath = "\\" + ip_address + "/" + path_to_server_file_folder
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    d = {
        filename: ((ftp.sendcmd("MDTM " + filename))[4:])
        for filename in filter(parent, only_files)
    }
    if not d:
        print("file not found, abort!")
        sys.exit("-1")
    else:
        find_files.append(max(d, key=lambda i: d[i]))
    if not find_files:
        print("file not found, abort!")
        sys.exit("-1")
    file_name = (
        "\\" + ip_address + " / " + path_to_server_file_folder + "/" + find_files[0]
    )
    # file_name = path_to_server_file_folder + "/" + find_files[0]
    return file_name


def connect_to_server(login, password):
    """
    Connect to server using login/password
    :param login: login (string)
    :param password: password (string)
    :return: None.
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((ip_address, port_no))
    clientsocket.send(login)
    # print(clientsocket.recv(1024)) # commented-out to supress debug output
    clientsocket.send(password)
    # print(clientsocket.recv(1024)) # commented-out to supress debug output
    return


def user_input():
    """
    Get user input: ip address, mask, file name, num pattern

    :return: None.
    """
    global num_pattern
    print("Enter IP address of server: ")
    ip_address = input()
    check_ip_address_existence(ip_address)
    print("Enter file mask: ")
    file_mask = input()
    # Using local method
    file_name = check_file_existence_re_loc(file_mask)
    # Comment-out FTP method
    # file_name = check_file_existence_re_loc(file_mask)
    print("Enter num ID: ")
    num_pattern = int(input())
    return


def find_first_match():
    """
    Find number of first line with pattern match, return -1 if not found

    :return: number of first line with pattern match, return -1 if not found
    """
    counter = 0
    # we're using utf-8 encoding, but can be changed to any
    global num_pattern
    with io.open(file_name, encoding="utf-8") as file:
        for line in file:
            counter += 1
            if str(num_pattern) in line:
                file.close()
                return counter
    file.close()
    return -1


def print_area(line_start, line_end):
    """
    Print area of the grepped log from start to end line

    :param line_start: line start (first)
    :param line_end:  line end (last)
    :return: None.
    """
    # we don't care if lineStart or lineEnd will be out of bounds
    # because these conditions is not reachable by our loop
    lines = [i for i in range(line_start, line_end)]
    i = 0
    f = open(file_name)
    for line in f:
        if i in lines:
            print(line, end=" ")
        i += 1
    return


# calling function
def find_logs():
    """
    Calling function

    :return: None
    """
    user_input()
    first_match_line = find_first_match()
    if first_match_line == -1:
        print("Pattern not found in file!")
    else:
        print_area(first_match_line - 100, first_match_line + 100)
    return


# start
find_logs()
