import os.path
import sys  

def ip_file_valid():

    file = input("\nenter file path :")

    if os.path.isfile(file) == True:
        print("file is valid")
    else:
        print(f"{file} the file does not exit",)
        sys.exit()

    with open(file,"r") as ip_file :
        ip_file.seek(0)
        ip_list = ip_file.readlines()

    return ip_list

list = ip_file_valid()
print(list)
