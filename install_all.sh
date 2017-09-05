#!/bin/bash


## Centos 7

#  nuttcp
## without inetd support
sudo su - 
yum install -y python3 python-software-properties software-properties-common wget bzip2 make gcc
cd /tmp
wget http://nuttcp.net/nuttcp/nuttcp-8.1.4.tar.bz2
bzip2 -d nuttcp-8.1.4.tar.bz2
tar -xvf nuttcp-8.1.4.tar
mv nuttcp-8.1.4 /opt
cd /opt/nuttcp-8.1.4
make
ln -sf  /opt/nuttcp-8.1.4/nuttcp-8.1.4 /usr/local/bin/nuttcp
mkdir /opt/nuttcp_workspace
sed -i '365i  nuttcp          5000/tcp \nnuttcp-data     5001/tcp \nnuttcp6         5000/tcp \nnuttcp6-data    5001/tcp' /etc/services
/usr/local/bin/nuttcp -S


#  dtn_monitor
sudo su - 
yum update
yum install https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm  # to fix node6js
yum -y install python-pip ansible git  python-dev libzmq3-dev npm nodejs-legacy  pciutils libfreetype6-dev python34-pip python34-devel 
npm install -g configurable-http-proxy
pip3 install jupyterhub notebook paramiko psutil numpy pymongo matplotlib
pip3 install --upgrade matplotlib pip




## ubuntu 
#  nuttcp
apt-get update
apt-get install -y python3 python-software-properties software-properties-common openbsd-inetd wget bzip2 make gcc
cd /tmp
wget http://nuttcp.net/nuttcp/nuttcp-8.1.4.tar.bz2
bzip2 -d nuttcp-8.1.4.tar.bz2
tar -xvf nuttcp-8.1.4.tar
mv nuttcp-8.1.4 /opt
cd /opt/nuttcp-8.1.4
make
ln -sf  /opt/nuttcp-8.1.4/nuttcp-8.1.4 /usr/local/bin/nuttcp
mkdir /opt/nuttcp_workspace
echo "nuttcp  stream  tcp     nowait  root    /usr/sbin/tcpd  /usr/local/bin/nuttcp -S" >> /etc/inetd.conf
sed -i '365i  nuttcp          5000/tcp \n nuttcp-data     5001/tcp \n nuttcp6         5000/tcp \n nuttcp6-data    5001/tcp' /etc/services
service openbsd-inetd restart

#  dtn_monitor

apt-get update
apt-get -y install python-pip python3-pip ansible git python3-dev python-dev libzmq3-dev npm nodejs-legacy python3-matplotlib pciutils libfreetype6-dev
npm install -g configurable-http-proxy
pip3 install jupyterhub notebook paramiko psutil numpy pymongo
pip3 install --upgrade matplotlib
