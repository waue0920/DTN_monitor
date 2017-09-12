import time
import sys
import subprocess


def main():
    while True:
        proc1 = subprocess.Popen(["./dtnscript.sh"], shell=True, stdout=None)

        time.sleep(8)


main()
