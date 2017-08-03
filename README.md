# DTN_monitor

DTN_only/
* DTN_monitor.ipynb (Jupyter notebook)
* dtnmonitor.py (main entrance for jupyter UI. include download(), because it needs to show current frame)
* bandw.py (monitor graph)
* calldtnscript.py (call dtnscript.sh)
* dtnscript.sh (write dtn information to mongoDB)
* downloadncar.py (download example)
* monitor(CPU, mem, network, IO data generated from bandw.py)
* NOAA/ (download data will be saved here)
  * grib2	(original)

![architecture](https://raw.githubusercontent.com/waue0920/DTN_monitor/master/graph/archi.png)


# 1. Jupyterhub Environment Setting

## prerequirement 
* note : this scripts was tested on Ubuntu 16.04 upper
* note : dtnscript.sh and downloadncar.py need fill correct username/password information, contact us about the detail. 

## Update source
sudo apt-get   update

## Install python-pip python3-pip and ansible
sudo  apt-get  -y  install  python-pip  python3-pip ansible git

## Install libzmq3, python and python3 develop packages
sudo  apt-get  -y install  python3-dev  python-dev libzmq3-dev

## Instll nodejs package manager for next step
sudo  apt-get -y  install   npm   nodejs-legacy

## Use npm install http proxy
sudo  npm   install   -g  configurable-http-proxy

## Use pip3 install jupyterhub and notebook 
sudo   pip3   install   jupyterhub

sudo   pip3   install   notebook

sudo   pip3   install   paramiko

# 2. Install	Python library

*	matplotlib: 

sudo apt-get install python3-matplotlib

*	psutil (for monitor data): 

sudo pip3 install psutil

*	numpy: 

sudo pip3 install numpy

*	pymongo

sudo pip3 install pymongo

*	lspci

sudo apt-get install pciutils

* note : if your OS version = ubuntu 14.04, you need to follow next step to trouble shoot the graph error

>add to .config/matplotlib/matplotlibrc line backend : Agg
>sudo apt-get install libfreetype6-dev
>sudo pip3 install --upgrade matplotlib

# 3. Usage

1.	Copy folder DTN_only to your home directory

cd ~

git clone https://github.com/waue0920/DTN_monitor.git

2.	Start Jupyterhub

sudo jupyterhub

3.	Open web browser  http://<your IP>:8000/
4.	Sign in as your user/passwd on linux server
5.	Import DTN_monitor.ipynb 
6. Execute jupyter notebook step by step 

![architecture](https://raw.githubusercontent.com/waue0920/DTN_monitor/master/graph/jupyter.png)

## Author Information: 
Peggy Lu (peggylu@narlabs.org.tw)

