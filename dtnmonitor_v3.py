import psutil
import time
import sys, os
import numpy
import matplotlib.pyplot as plt
import threading
import datetime
from IPython import display

class DTNMonitor:

    def __init__(self):
        self.network_monitor_list = []
        self.diskio_monitor_list = []
        self.cup_monitor_list = []
        self.mem_monitor_list = []
        self.interface = "all"
        
    def monitor_bandwidth(self):
        max_graph_point = 25
        old_value = 0
        disk_old_value = 0
        count = 0
        prev_t = 0
        time_diff = 0
        
        while self.running:
            curr_t = datetime.datetime.now()
            if self.interface == "all":
                new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            else:
                new_value = psutil.net_io_counters(pernic=True)[self.interface].bytes_sent + psutil.net_io_counters(pernic=True)[self.interface].bytes_recv

            disk_new_value = psutil.disk_io_counters().write_bytes + psutil.disk_io_counters().read_bytes
            
            if old_value == 0 :
                net = float(0)
                disk = float(0)
                #prev_t = curr_t
            else:
                delta_t = curr_t - prev_t
                time_diff = delta_t.seconds + delta_t.microseconds/1E6
                net = float(convert_to_mbit(new_value - old_value)) / time_diff
                disk = float(convert_to_mbyte(disk_new_value - disk_old_value)) / time_diff
            cpu = float(psutil.cpu_percent())
            mem = float(psutil.virtual_memory().percent)
    
            #print(net, self.network_monitor_list)
            self.network_monitor_list.append(net)
            self.diskio_monitor_list.append(disk)
            self.cup_monitor_list.append(cpu)
            self.mem_monitor_list.append(mem)
            
            count = count + 1
            old_value = new_value
            disk_old_value = disk_new_value
            prev_t = curr_t
            time.sleep(1)
            
    def draw_graph(self):

        while self.running:
        
            f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col')
            f.set_size_inches(15, 10)
            
            #print(self.network_monitor_list)
            netarr = numpy.array(self.network_monitor_list[-25:])
            diskarr = numpy.array(self.diskio_monitor_list[-25:])
            cpuarr = numpy.array(self.cup_monitor_list[-25:])
            memarr = numpy.array(self.mem_monitor_list[-25:])

            ax1.grid(alpha=0.5)
            ax1.set_title("Network Performance")
            ax1.set_xlabel('Sec')
            ax1.set_ylabel('Mb')

            ax2.grid(alpha=0.5)
            ax2.set_title("DISK IO")
            ax2.set_xlabel('Sec')
            ax2.set_ylabel('MB')

            ax3.grid(alpha=0.5)
            ax3.set_title("CPU Usage")
            ax3.set_xlabel('Sec')
            ax3.set_ylabel('Percentage')

            ax4.grid(alpha=0.5)
            ax4.set_title("Memory Usage")
            ax4.set_xlabel('Sec')
            ax4.set_ylabel('Percentage')
        
            ax1.plot(((netarr )))
            ax2.plot(((diskarr )), color="green")
            ax3.plot(((cpuarr)))
            ax4.plot(((memarr)))
            
            display.display(plt.show())
            display.clear_output(wait=True)
            
            
            time.sleep(1)


    def stop(self):
        self.running = False
        with open('netlog.txt','w') as f:
            for element in self.network_monitor_list:
                f.write('{}\n'.format(element))
            
    
    def run_monitor(self, timeout=None):
        self.network_monitor_list = []
        self.diskio_monitor_list = []
        self.cup_monitor_list = []
        self.mem_monitor_list = []
        
        
        try:
            self.running=True
            m_thread = threading.Thread(target=self.monitor_bandwidth)
            g_thread = threading.Thread(target=self.draw_graph)
            
            m_thread.start()
            g_thread.start()
            
            count = 0
            if timeout != None:
                while count < timeout:
                    time.sleep(1)
                    count += 1
                self.stop()
                
            
        except:
            self.stop()
        
def convert_to_mbyte(value):
    return (value / 1024. / 1024.)

def convert_to_mbit(value):
    return (value * 8 / 1024. / 1024. )

def send_stat(value):
    return convert_to_gbit(value)