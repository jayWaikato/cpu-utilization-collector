import paramiko 
import os.path
import datetime
import sys
import re
import time
import json


global devices

devices = {"10.10.10.2" : "arista1",
           "10.10.10.3" : "arista2",
           "10.10.10.4" : "arista3"} 

credential_file = input("enter credential file path ")
cpu_data_time = ""

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
    device = ''
    
    for key in devices:
        
        add_cpu_data  = {}
        # print(f"in looop {key} and {ip}")
        # print(f"type of key {type(key)} and type of ip { type(ip)}")
        # print(f"")

      
        ip = ip.rstrip("\n")
        if key == ip :
    
            device+=devices[key]

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
            print("device configuration is done for ip : {} , at time :  {}".format(ip,str(datetime.datetime.now())))

        cpu_usage = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)+us,",router_output)
        cpu_data_time  = re.search(b"top - (\d{2}:\d{2}:\d{2}) up",router_output).group(1).decode("utf-8")
     

        utilization = cpu_usage.group(2).decode("utf-8")
        add_cpu_data[cpu_data_time] = utilization

        with open("C:\\Users\\jaych\\Downloads\\cpu.json","r") as cpu_utilization :  
            data = json.load(cpu_utilization)

        if device in data:
            data[device].update(add_cpu_data)

            with open("C:\\Users\\jaych\\Downloads\\cpu.json","w") as update_file  :
                json.dump(data,update_file,indent=4)

        else:
            print(f"{device} could not be found.")

    
        # print(str(router_output)+ "\n")
        # print(re.findall('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',str(router_output)))

        connection.close()

        session.close()
    except paramiko.AuthenticationException :
        print("invalid username or password")


