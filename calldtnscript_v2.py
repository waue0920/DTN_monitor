import time
import sys
import subprocess


def main():
    while True:
        proc1 = subprocess.Popen(["./dtnscript_v2.sh"], shell=True, stdout=None)

        time.sleep(60)


main()
