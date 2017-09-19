import time
import psutil
import os, sys


# mode 0:all mode1:100pt
def main(mode, interface):
    #    mode=0
    print("mode=" + mode)
    max_graph_point = 100
    old_value = 0
    disk_old_value = 0
    data = []
    count = 0
    while True:
        if interface == "all":
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
        else:
            new_value = psutil.net_io_counters(pernic=True)[interface].bytes_sent + psutil.net_io_counters(pernic=True)[
                interface].bytes_recv

        disk_new_value = psutil.disk_io_counters().write_bytes + psutil.disk_io_counters().read_bytes
        if old_value:
            net = convert_to_mbit(new_value - old_value)
            disk = convert_to_mbyte(disk_new_value - disk_old_value)
            cpu = str(psutil.cpu_percent())
            mem = str(psutil.virtual_memory().percent)
            if count > 100 and int(mode) == 1:
                with open('monitor', 'r') as fin:
                    oldfile = fin.read().splitlines(True)
                    fin.close()
                with open('monitor', 'w') as fout:
                    fout.writelines(oldfile[1:])
                    fout.write(net + "," + disk + "," + cpu + "," + mem)
                    # fout.write(new_value+","+old_value+","+cpu+","+mem)
                    fout.write("\n")
                    fout.close()
            else:
                with open('monitor', 'a+') as f:
                    f.seek(0, 2)
                    f.write(net + "," + disk + "," + cpu + "," + mem)
                    # f.write(new_value+","+old_value+","+cpu+","+mem)
                    f.write("\n")
                    f.close()
        count = count + 1
        old_value = new_value
        disk_old_value = disk_new_value

        time.sleep(1)

def convert_to_mbyte(value):
    return ("%0.3f" % (value / 1024. / 1024.) )

def convert_to_mbit(value):
    return ("%0.3f" % (value * 8 / 1024. / 1024. ))


def send_stat(value):
    return ("%0.3f" % convert_to_gbit(value))


os.system("rm -f monitor")
file = open('monitor', 'w+')
file.close()

main(sys.argv[1], sys.argv[2])
