#!/bin/bash
### Readme ###
# 1. It is necessary for starting the Iperf3 server preliminarily.
# $  for i in $(seq 1 8 );do iperf3 -s -D -p 5300$i;done
# 2. Use the script to generate network traffic and calculate the throughput.
# ./gen_net_test.sh <server> <windows_size>
#

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
cd $bin;

mkdir -p ./logs

if [ "$2" != ""  ]
then
        server=$1
        size=$2
else
        echo "./gen_net_test.sh <server> <size>"
        exit 0

fi

for i in $(seq 1 8) ;do 
         xx="iperf3 -w $size -Z -t 10 -f g  -c $server -p 5300${i}" 
         exec $xx >./logs/${server}_a${i}.log 2>&1 &
done

sleep 15

tail -n 5 ./logs/${server}_a*.log |grep sender

sum=0
for i in $(tail -n 5 ./logs/${server}_a*.log |grep sender |awk {'print $7'});do 
         sum=$(echo "print ${sum} + ${i}" | python ) 
done
echo $sum Gbits/sec

