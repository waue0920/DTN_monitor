#!/bin/bash

apt-get update
apt-get -y install python-pip python3-pip ansible git python3-dev python-dev libzmq3-dev npm nodejs-legacy python3-matplotlib pciutils libfreetype6-dev
npm install -g configurable-http-proxy
pip3 install jupyterhub notebook paramiko psutil numpy pymongo
pip3 install --upgrade matplotlib
