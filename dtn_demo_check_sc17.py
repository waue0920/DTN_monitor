#!/usr/bin/env python3
### readme
### run the script in sudoer priviledge ! ( or get exception)

#
# json_str = json.dumps(data)
#
# print(json_str)
#
# with open('data.json', 'w') as f :
#    json.dump(data,f)
#
# with open('data.json', 'r') as f :
#    data1 = json.load(f)
#
# from pprint import pprint
# pprint(data1)

import json
import pprint
import os
import subprocess
import re
import shutil
import socket


### Using os.system(..) to execute cmd and return 0 or 1
### Using subprocess.Popen(..) to get the execution result
def return_command(cmd):
    #  return execution result as output -> str
    process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=1)
    return process.stdout.read().decode('utf8')

def check_command(cmd):
    #  return 0 if success, or return > 0 -> int
    return os.system(cmd)


def checkFirewall():
    # check iptables is existed, if without iptables, pass the check
    if shutil.which("iptables") is None:
        return 1

    ret = return_command("head -n 1 /etc/os-release")
    # check Centos or Ubuntu, only Centos iptables filter 8000 ..
    # if re.search("CentOS Linux", ret) == None: # easily failed
    if "CentOS" in ret :
        # if Centos , check the rule for opening 8000 port for jupyter
        ret = return_command("iptables -nvL |grep 8000 |wc -l")
        if int(ret) < 1:
            return 0
    return 1


def checkVlan():
    vlan63 = "192.168.63.59"
    vlan61 = "192.168.61.57"
    # check vlan 61 and 63
    if int(check_command("ping -c 1 " + vlan63 + ">/dev/null")) != 0:
        # vlan 63 can't connect, check 61
        if int(check_command("ping -c 1 " + vlan61 + ">/dev/null")) != 0:
            # neither 61 nor 63 is failed to ping, return 0
            return 0
        else :
            return 61
    else :
        # vlan 63 ok , check 61
        if int(check_command("ping -c 1 " + vlan61 + ">/dev/null")) != 0:
            # vlan 63 ok, check 61 failed
            return 63
        else:
            # both 61 nor 63 is ok to ping
            return 6163


def checkJupyter():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # check the jupyter port is open, because system reboot will reset iptables rules
    ret = sock.connect_ex(('0.0.0.0', 8000))
    if ret != 0:
        return 0
    return 1


def checkNvme():
    ret = int(return_command("df |grep nvme |wc -l "))
    if type(ret) == int :
        return int(ret)
    else :
        return 0


def checkFileExist():
 ### this will occur file not found exection
 #   ret = return_command("ls /data/disk*/sc17/fftest | wc -l ")
 #   if int(ret) < 8:
 #       return 0
 #   return 1
    count=0
    dirlist = [
        "/data/disk0/sc17/fftest",
        "/data/disk1/sc17/fftest",
        "/data/disk2/sc17/fftest",
        "/data/disk3/sc17/fftest",
        "/data/disk4/sc17/fftest",
        "/data/disk5/sc17/fftest",
        "/data/disk6/sc17/fftest",
        "/data/disk7/sc17/fftest",
    ]
    for fd in dirlist:
        if os.access(fd, os.R_OK) is False:
            continue
        count+=1
    return count

def checkDirPermission():
    count=0
    dirlist = [
        "/data/disk0/sc17/",
        "/data/disk1/sc17/",
        "/data/disk2/sc17/",
        "/data/disk3/sc17/",
        "/data/disk4/sc17/",
        "/data/disk5/sc17/",
        "/data/disk6/sc17/",
        "/data/disk7/sc17/",
    ]
    for fd in dirlist:
        if os.access(fd, os.W_OK) is False:
            continue
        count+=1
    return count


checklist = {}


# checklist = {
#    'firewall_check': 1,
#    'vlan_check': 1,
#    'jupyter_check': 1,
#    'nvme_check': 1,
#    'directory_check': 1,
#    'permission_check': 1,
# }


def checkSudoer():
    if os.getuid() != 0 :
        return False
    else :
        return True

def main():
    checklist["firewall_check"] = checkFirewall()
    checklist["vlan_check"] = checkVlan()
    checklist["jupyter_check"] = checkJupyter()
    checklist["nvme_check"] = checkNvme()
    checklist["testfile_check"] = checkFileExist()
    checklist["permission_check"] = checkDirPermission()
    json_str = json.dumps(checklist,indent=4)
    print(json_str)
    with open("./dtn_demo_check_sc17.json","w") as f :
        f.write(json_str)



if __name__ == "__main__":
    if checkSudoer() is False:
        print("{msg=\"You should run this in sudo priviledge !\"}")
        exit(1)
    main()

