#!/bin/bash
#WORKERS="192.168.111.73 192.168.111.101 192.168.111.99 192.168.111.100"
#MACHINE_NAME=`hostname`
MACHINE_NAME="bonnie-vm4"
echo 3 | tee /proc/sys/vm/drop_caches &&  sync
sleep 5
rm -rf /mnt/vd*/Bonnie.*
bonnie++ -p -1 -u0
bonnie++ -p$1 -u0
IN=$1
NN=0
EE=$((IN-1))
for disk in `lsblk  | grep -vE "vda|NAME" | cut -d " " -f1`; do 
 if [[ $NN == $1 ]]; then exit; fi 
 if [[ $NN == $EE ]]; then 
 bonnie++ -y s -s 8192 -r 4096 -u root -d /mnt/${disk}/ -m ${MACHINE_NAME} > /root/bonnie/bonnie_distr_${MACHINE_NAME}_${disk}_$1.log
 else
 bonnie++ -y s -s 8192 -r 4096 -u root -d /mnt/${disk}/ -m ${MACHINE_NAME} > /root/bonnie/bonnie_distr_${MACHINE_NAME}_${disk}_$1.log &
 fi
((NN+=1))
done
