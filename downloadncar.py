#!/usr/bin/pythoni
from multiprocessing import Process,Value
import time
import errno    
import sys
import os
import subprocess
from os import path   

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

import subprocess
import shutil
def execute(command):

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        nextline = process.stdout.readline()
        sys.stdout.write(nextline)

def authenticate(username,passwd):
 #user authorized
    authen_command = 'wget --no-check-certificate -O Authentication.log --save-cookies auth.rda_ucar_edu --post-data="email='+username+'&passwd='+passwd+'&action=login" https://rda.ucar.edu/cgi-bin/login '
    execute(authen_command)

def download(date,simu_starttime,folder):

    output_directory=folder+"/"+date+"_"+simu_starttime

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    origin_folder =output_directory+"/grib2"
    mkdir_p(origin_folder)

    year=date[0:4]

    number=0

    while (number <=384):  
        number_str=("%03d" %(number))
        url="http://rda.ucar.edu/data/ds084.1/"+year+"/"+date+"/gfs.0p25."+date+simu_starttime+".f"+number_str+".grib2"
        global filename
        filename="starting to download file "+date+" "+number_str
   #     print("starting to download "+url+".....")
        wget_command = 'wget -N --no-check-certificate --load-cookies auth.rda_ucar_edu '+url+" -P "+origin_folder
        #os.system(wget_command)
        cmd = wget_command.split()
        subprocess.call(cmd)
#        execute(wget_command)

        if (number<240):
            number=number+3
        else: 
            number=number+12


   
def main(argv):

    date=argv[0] #"20170428" #enter dates between previous 2 years
    simu_starttime=argv[1]#"00"  #00 06 12 18
    folder=argv[2]

    username = "peggy@northwestern.edu"
    passwd="1234"


    authenticate(username,passwd)

    download(date,simu_starttime,folder)


if __name__ == "__main__":
   main(sys.argv[1:])
