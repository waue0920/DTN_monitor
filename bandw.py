import time
import psutil
import os, sys


# mode 0:all mode1:100pt
time_sleep = 3
#title="default"
current_time_stemp = time.time()
def main(mode, interface,title):
    #    mode=0
    print("mode=" + mode)
    max_graph_point = 100
    old_value = 0
    disk_old_value = 0
    data = []
    count = 0
    try:
        os.remove("monitor_"+title)
    except OSError:
        pass

    while True:

        if interface == "all":
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            #new_nrec_value = psutil.net_io_counters().bytes_recv
            #new_nsnt_value = psutil.net_io_counters().bytes_sent
        else:
            new_value = psutil.net_io_counters(pernic=True)[interface].bytes_sent + psutil.net_io_counters(pernic=True)[
                interface].bytes_recv

        disk_new_value = psutil.disk_io_counters().write_bytes + psutil.disk_io_counters().read_bytes

        if old_value:

            net = convert_to_mbit(new_value - old_value )
            #net_rec = convert_to_mbit(new_nrec_value - old_nrec_value)
            #net_send = convert_to_mbit(new_nsnt_value - old_nsnt_value)
            disk = convert_to_mbyte(disk_new_value - disk_old_value)
            cpu = str(psutil.cpu_percent())
            mem = str(psutil.virtual_memory().percent)
            if count > 100 and int(mode) == 1:
                with open("monitor_"+title, 'r') as fin:
                    oldfile = fin.read().splitlines(True)
                    fin.close()
                with open("monitor_"+title, 'w') as fout:
                    fout.writelines(oldfile[1:])
                    fout.write(net + "," + disk + "," + cpu + "," + mem)
                    #fout.write(net + "," + net_rec + "," + net_send + "," + disk + "," + cpu + "," + mem)
                    # fout.write(new_value+","+old_value+","+cpu+","+mem)
                    fout.write("\n")
                    fout.close()
            else:
                with open("monitor_"+title, 'a+') as f:
                    f.seek(0, 2)
                    f.write(net + "," + disk + "," + cpu + "," + mem)
                    #f.write(net + "," + net_rec + "," + net_send + "," + disk + "," + cpu + "," + mem)
                    # f.write(new_value+","+old_value+","+cpu+","+mem)
                    f.write("\n")
                    f.close()
        count = count + 1
        old_value = new_value
        #old_nsnt_value = new_nsnt_value
        #old_nrec_value = new_nrec_value
        disk_old_value = disk_new_value

        time.sleep(time_sleep)
        current_time_stemp = time.time()


def convert_to_mbit(value):
    duration=time.time() - current_time_stemp
    return ("%0.3f" %(value * 8 / 1024. / 1024. / (time_sleep + duration)))


def convert_to_mbyte(value):
    duration = time.time() - current_time_stemp
    print("duration %r"%(duration))
    return ("%0.3f" %(value / 1024. / 1024. / (time_sleep + duration)))


#os.system("rm -f monitor_"+sys.argv[3])
#file = open('monitor', 'w+')
#file.close()

main(sys.argv[1], sys.argv[2],sys.argv[3])
