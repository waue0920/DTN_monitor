import itertools
import psutil
import time
import sys, os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import threading
import datetime
from IPython import display
import csv
from multiprocessing import Process
import errno
from os import path

interface = "all"



class Graph(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        #        global filename
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
        while not self.killed:
            network_monitor_list = []
            diskio_monitor_list = []
            cup_monitor_list = []
            mem_monitor_list = []
            with open('monitor') as f:
                # for line in f:
                #    monitor_list.append(line.strip())
                reader1, reader2 = itertools.tee(csv.reader(f, delimiter=","))
                for row in reader2:
                    if (len(next(reader1)) != 4):
                        continue

                    #                for row in csv.DictReader(f, ['network', 'diskio', 'cpu', 'mem']):
                    #                   if(len(row) !=4):
                    #                      continue

                    network_monitor_list.append(row[0].strip())
                    diskio_monitor_list.append(row[1].strip())
                    cup_monitor_list.append(row[2].strip())
                    mem_monitor_list.append(row[3].strip())
            # print network_monitor_list
            netarr = np.array(network_monitor_list, dtype=float)
            diskarr = np.array(diskio_monitor_list, dtype=float)
            cpuarr = np.array(cup_monitor_list, dtype=float)
            memarr = np.array(mem_monitor_list, dtype=float)
            # fig , ax= plt.subplots(dpi=80)
            # f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
            f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')
            f.set_size_inches(15, 10)
            #            f.suptitle(filename, fontsize=30)
            ax1.plot(((netarr )))
            ax1.grid(alpha=0.5)
            ax1.set_title("Network Performance")
            ax1.set_xlabel('Sec')
            ax1.set_ylabel('Mb')

            ax2.plot(((diskarr )), color="green")
            ax2.grid(alpha=0.5)
            ax2.set_title("DISK IO")
            ax2.set_xlabel('Sec')
            ax2.set_ylabel('MB')

            ax3.plot(((cpuarr)))
            ax3.grid(alpha=0.5)
            ax3.set_title("CPU Usage")
            ax3.set_xlabel('Sec')
            ax3.set_ylabel('Percentage')

            ax4.plot(((memarr)))
            ax4.grid(alpha=0.5)
            ax4.set_title("Memory Usage")
            ax4.set_xlabel('Sec')
            ax4.set_ylabel('Percentage')

            display.display(plt.show())
            display.clear_output(wait=True)
            # plt.show()
            time.sleep(0.5)

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


## just exec method
def exec_run(command):
    subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)


## bad print method, just work but one line
# def exec_print(command):
#    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
#    (out, err) = proc.communicate()
#    print("out:", out)

## good print method, 
def exec_sysout(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        nextline = process.stdout.readline()
        sys.stdout.write(nextline)


## good print method, be note that logfile must set
# def exec_print_log(command):
#  with open(logfile, 'a') as f:
#      process = subprocess.Popen([command], stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
#      f.write("\n# command: " + command + "(time:" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")\n")
#      for line in iter(process.stdout.readline, b''):
#          # system print
#          sys.stdout.write(line)
#          # log
#          f.write(line.decode(sys.stdout.encoding) )


def monitorit(func):
    def my_wrap(*args, **kwargs):
        #       procmongo = Process(target=dtn2db)
        procmongo = subprocess.Popen(["python3", "calldtnscript_v2.py"], stdin=subprocess.PIPE)
        if args is None:
            mode = 1
        else:
            mode = args[1]
        #        procmongo.start()
        #       procmongo.join()
        proc = subprocess.Popen(["python3", "bandw.py", str(mode), interface], stdout=subprocess.PIPE)
        time.sleep(1)

        thread = Graph()
        thread.daemon = True
        thread.start()
        out = func(*args, **kwargs)
        time.sleep(8)
        proc.kill()
        procmongo.kill()
        thread.kill()

    return my_wrap


@monitorit
def exec_command(cmd, mode):
    #    mode=input_mode
    cmd = cmd.split()
    if cmd is not None:
        #    global filename

        try:
            # download(date,time,folder)
            subprocess.call(cmd)
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exc_info() == (None, None, None)


# sys.exc_clear()

@monitorit
def start_monitor(cmd, mode):
    #    mode=input_mode
    try:
        # download(date,time,folder)
        #    subprocess.call(cmd)
        print(cmd)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exc_info() == (None, None, None)

## start_monitor not used
# sys.exc_clear()
