import paramiko 
import os.path
import time
import sys
import re

credential_file = input("enter credential file path ")

if os.path.isfile(credential_file) == True :
    print("file is valid")
else :
    print(f"{credential_file} file does not exists.")
    sys.exit()

cmd_file = input("enter commands file path")

if os.path.isfile(cmd_file) == True:
    print("file is valid")
else:
    print(f"{cmd_file} file is inbvalid")
    sys.exit()

def ssh_connection(ip):

    global cmd_file
    global credential_file

    try:
        with open(credential_file, "r") as user_file:
            user_file.seek(0)
            username = user_file.readlines()[0].split(',')[0].rstrip('\n')
            user_file.seek(0)
            password = user_file.readlines()[0].split(',')[1].rstrip('\n')

        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(ip.rstrip("\n"),username=username,password=password)
        connection = session.invoke_shell()
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)

        connection.send("configure terminal \n")
        time.sleep(1)

        with open(cmd_file,"r") as commands :
            commands.seek(0)

            for each_line in commands.readlines():
                connection.send(each_line + "\n")
                time.sleep(2)

        router_output = connection.recv(65535)

        if re.search(b"% Invalid input", router_output):
            print("invalid input or syntex error")
        else:
            print("device configuration is done")

        print(str(router_output)+ "\n")

        connection.close()

        session.close()
    except paramiko.AuthenticationException :
        print("invalid username or password")

