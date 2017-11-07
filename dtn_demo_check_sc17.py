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
    process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    return process.stdout.read().decode('utf8')

def check_command(cmd):
    #  return 0 if success, or return > 0 -> int
    return os.system(cmd)


def checkFirewall():
    # check iptables is existed, if without iptables, pass the check
    if shutil.which("iptables") is None:
        return True

    ret = return_command("head -n 1 /etc/os-release")
    # check Centos or Ubuntu, only Centos iptables filter 8000 ..
    # if re.search("CentOS Linux", ret) == None: # easily failed
    if "CentOS" in ret :
        # if Centos , check the rule for opening 8000 port for jupyter
        print("is centos, check iptables")
        ret = return_command("iptables -nvL |grep 8000 |wc -l")
        if int(ret) < 1:
            return False
    return True


def checkVlan():
    vlan63 = "192.168.63.59"
    vlan61 = "192.168.61.57"
    # check vlan 61 and 63
    if int(check_command("ping -c 1 " + vlan63)) != 0:
        # vlan 63 can't connect, check 61
        if int(check_command("ping -c 1 " + vlan61)) != 0:
            # neither 61 nor 63 is failed to ping, return false
            return False
    return True


def checkJupyter():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # check the jupyter port is open, because system reboot will reset iptables rules
    ret = sock.connect_ex(('0.0.0.0', 8000))
    if ret != 0:
        return False
    return True


def checkNvme():
    ret = return_command("df |grep nvme |wc -l ")
    if int(ret) < 8:
        return False
    return True


def checkFileExist():
 ### this will occur file not found exection
 #   ret = return_command("ls /data/disk*/sc17/fftest | wc -l ")
 #   if int(ret) < 8:
 #       return False
 #   return True

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
            return False
    return True

def checkDirPermission():
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
            return False
    return True


checklist = {}


# checklist = {
#    'firewall_check': True,
#    'vlan_check': True,
#    'jupyter_check': True,
#    'nvme_check': True,
#    'directory_check': True,
#    'permission_check': True,
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
    json_str = json.dumps(checklist)
    pprint.pprint(json_str)


if __name__ == "__main__":
    if checkSudoer() is not True :
        print("You should run this in sudo priviledge !")
        print("exit 1")
        exit(1)
    main()

