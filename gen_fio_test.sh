#!/bin/bash
bin=`dirname "$0"`
bin=`cd "$bin"; pwd`
cd $bin;

NUM=7
#USER=$(whoami)
USER=sc17

function p_mkdir(){
echo "Gen testDIR (!!! run it by sudoer !!!)"
#echo $'for i in $(seq 0 '$NUM') ;do sudo mkdir -p /data/disk${i}/'${USER}'; sudo chown '${USER}':'${USER}' /data/disk${i}/'${USER}' ; done'
for i in $(seq 0 $NUM) ;do sudo mkdir -p /data/disk${i}/${USER}; sudo chown ${USER}:${USER} /data/disk${i}/${USER} ; done
ls -al /data/disk*/${USER}
}

function p_test_write(){
echo "Gen write:  (a few minutes....)"
for i in $(seq 0 $NUM);do 
   xx="fio --thread --rw=write --norandommap --group_reporting --time_based  --randrepeat=0 --bs=1M --ioengine=posixaio --runtime=30 --iodepth=32 --name=drive0 --size=100G  --filename=/data/disk"$i"/${USER}/fftest"; 
   if [ $i != "$NUM" ]; then
	echo "$xx >./w${i}.log 2>&1 &"
	exec $xx >./w${i}.log 2>&1 & 

   else 
        #xx="fio --thread --rw=write  --norandommap --group_reporting --time_based  --randrepeat=0 --bs=1M --ioengine=sync  --runtime=30 --iodepth=32 --name=drive0 --size=100G  --filename=/data/disk"$i"/waue/fftest";
        echo "$xx | tee ./w${i}.log"
        exec $xx | tee ./w${i}.log

   fi
done

sleep 3
echo "=========="
p_result_write

}

function p_result_write(){
cat w*.log  |grep WRITE
add=0
for i in $(cat w*.log  |grep WRITE | awk {'print $2'} |sed s/bw=//g|sed s/M.*$//g);do
   add=$(($add+$i));
done
echo \"$add MiB/s\"

}


function p_result_read(){
cat r*.log  |grep READ
add=0
for i in $(cat r*.log  |grep READ | awk {'print $2'} |sed s/bw=//g|sed s/M.*$//g);do
   add=$(($add+$i));
done
echo \"$add MiB/s\"

}


function p_test_read(){
echo "Gen read : "
##v1. just echo
##for i in $(seq 0 7);do xx="fio --thread --rw=read --readonly  --norandommap --group_reporting --time_based  --randrepeat=0 --bs=1M --ioengine=sync  --runtime=30 --iodepth=32 --name=drive0 --size=100G  --filename=/data/disk"$i"/waue/fftest >./"$i".log 2>&1 &"; echo $xx ; done
##v2. execute
#for i in $(seq 0 7);do 
#	xx="fio --thread --rw=read --readonly --norandommap --group_reporting --time_based  --randrepeat=0 --bs=1M --ioengine=sync  --runtime=30 --iodepth=32 --name=drive0 --size=100G  --filename=/data/disk"$i"/waue/fftest"; 
#	exec $xx >./r${i}.log 2>&1 & 
#done
##v3. seperate run
for i in $(seq 0 $NUM);do
   xx="fio --thread -rw=read --readonly --norandommap --group_reporting --time_based  --randrepeat=0 --bs=1M --ioengine=sync  --runtime=30 --iodepth=32 --name=drive0 --size=100G  --filename=/data/disk"$i"/${USER}/fftest";
   if [ $i != "$NUM" ]; then
	echo "$xx >./r${i}.log 2>&1 &"
        exec $xx >./r${i}.log 2>&1 &
   else
        #xx="fio --thread --rw=write  --norandommap --group_reporting --time_based  --randrepeat=0 --bs=1M --ioengine=sync  --runtime=30 --iodepth=32 --name=drive0 --size=100G  --filename=/data/disk"$i"/waue/fftest";
        echo "$xx | tee ./r${i}.log"
        exec $xx | tee ./r${i}.log
   fi
done

sleep 3
echo "=========="
p_result_read

}

function p_result(){
#echo "Check result"
#echo "cat r*.log  |grep READ"
#echo $'add=0; for i in $(cat r*.log  |grep READ | awk {\'print $2\'} |sed s/bw=//g|sed s/M.*$//g);do add=$(($add+$i)); done ; echo \"$add MiB/s\"'
p_result_read


#echo $'cat w*.log  |grep WRITE'
#echo $'add=0; for i in $(cat w*.log  |grep WRITE | awk {\'print $2\'} |sed s/bw=//g|sed s/M.*$//g);do add=$(($add+$i)); done ; echo \"$add MiB/s\"'
p_result_write

}


case ${1} in
  "result")
        p_result
        ;;
  "twrite")
        p_test_write
        ;;
  "tread")
        p_test_read
        ;;
  "mkdir")
        p_mkdir
        ;;
  *)
        echo "Usage  ${0} {mkdir|twrite|tread|result}"
        echo "ex: ${0} twrite "
        ;;
esac

