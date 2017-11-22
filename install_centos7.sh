#!/bin/bash


## Centos 7

#  nuttcp
## without inetd support
yum install -y python3 python-software-properties software-properties-common wget bzip2 make gcc iperf3;
cd /tmp;
wget http://nuttcp.net/nuttcp/nuttcp-8.1.4.tar.bz2;
bzip2 -d nuttcp-8.1.4.tar.bz2;
tar -xvf nuttcp-8.1.4.tar;
mv nuttcp-8.1.4 /opt;
cd /opt/nuttcp-8.1.4;
make;
ln -sf  /opt/nuttcp-8.1.4/nuttcp-8.1.4 /usr/local/bin/nuttcp;
wget http://nuttcp.net/nuttcp/beta/nuttscp-2.3; chmod 755 nuttscp-2.3;cp nuttscp-2.3 /usr/local/bin/nuttscp;
ln -sf /opt/nuttcp-8.1.4 /opt/nuttcp;
mkdir /opt/nuttcp_workspace;


#  dtn_monitor

## install python34 for centos6 or centos7 if needed
#yum install -y epel-release
#yum install -y python34
#yum install -y python34-setuptools
#easy_install-3.4 pip
#pip3 install virtualenv


## install jupyterhub
yum update;
yum install https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm ; # to fix nodejs
yum -y install python34-devel libzmq3-dev openssl git npm nodejs-legacy  pciutils libfreetype6-dev python34-pip python34-devel ;
npm install -g configurable-http-proxy;
pip3 install jupyterhub notebook paramiko psutil numpy pymongo matplotlib netifaces;
pip3 install --upgrade pip;



## if jupyterhub conflict with SELinux
# echo "c.PAMAuthenticator.open_sessions = False" >> ~/jupyterhub_config.py
# jupyterhub -f ~/jupyterhub_config.py


## don't forgot to assign the account/passwd in config.sh

### optional

sudo echo "sc17    ALL=NOPASSWD:/usr/sbin/mlnx_tune,/usr/sbin/setpci" >> /etc/sudoers;
