#!/bin/bash

bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
cd $bin;

source ./config.sh

user="_temp_"
timestamp=`date +%s`
dbname="test"
#mongoUser=""
#mongoPwd=""
#mongoIP=""
collections="dtnInfo"

declare -A CPUArr
getCPUInfo()
{
  #declare -A arr
  the_list=`lscpu`

  while read line
    do
	mapName=$(echo $line|cut -d':' -f 1| tr -d "() -");
	value=$(echo $line|cut -d':' -f 2);
       
        CPUArr[$mapName]=`echo $value| awk '$1=$1'`

  done<<<"$the_list"
#  return arr
}

getSysctlInfo()
{
  CPUArr[net_core_rmem_max]=`sysctl -n net.core.rmem_max`
  CPUArr[net_ipv4_wmem_max]=`sysctl -n net.core.wmem_max`
  CPUArr[net_ipv4_tcp_rmem]=`sysctl -n net.ipv4.tcp_rmem`
  CPUArr[net_ipv4_tcp_wmem]=`sysctl -n net.ipv4.tcp_wmem`
  CPUArr[net_ipv4_tcp_congestion_control]=`sysctl -n net.ipv4.tcp_congestion_control`
  CPUArr[net_ipv5_tcp_mtu_probing]=`sysctl -n net.ipv4.tcp_mtu_probing`
}

getUsageInfo()
{
  CPUArr[memory_usage]=`free -m | awk 'NR==2{printf "%s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'`
  CPUArr[disk_usage]=`df -h | awk '$NF=="/"{printf "%d/%dGB (%s)\n", $3,$2,$5}'`
  CPUArr[CPU_load]=`top -bn1 | grep load | awk '{printf "%.2f\n", $(NF-2)}'`
}

getOthers()
{
#  CPUArr[manufacturer]=`dmidecode -t system|grep Manufacturer`
  CPUArr[vm]=`lspci | grep "System peripheral"|head -n 1|awk '{printf "%s %s\n", $4, $5}'`
}

getCPUInfo
getSysctlInfo
getUsageInfo
getOthers

outputJSname=$user$timestamp.py

echo -e 'import pymongo
\n
client = pymongo.MongoClient("mongodb://'$mongoUser':'$mongoPwd'@'$mongoIP'/'$dbname'")
\n
db = client.'$dbname'
\n
 '>>$outputJSname

echo "result = db.$collections.insert_one( { ">>$outputJSname
arrNum=${#CPUArr[@]}

count=0
for i in "${!CPUArr[@]}"
do
	if [ $count -eq $((arrNum-1)) ] ; then
		echo	\"$i\":\"${CPUArr[$i]}\">>$outputJSname
	else
		echo   \"$i\":\"${CPUArr[$i]}\",>>$outputJSname
	fi
	count=$((count+1))
done

echo -e "} )">>$outputJSname



python3 $outputJSname

rm $outputJSname

