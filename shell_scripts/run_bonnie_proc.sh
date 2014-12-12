#!/bin/bash
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
 bonnie++ -y s -s 8192 -r 4096 -u root -d /mnt/${disk}/ -m bonnie-vm1 > /root/bonnie/bonnie_${disk}_$1.log
 else
 bonnie++ -y s -s 8192 -r 4096 -u root -d /mnt/${disk}/ -m bonnie-vm1 > /root/bonnie/bonnie_${disk}_$1.log &
 fi
((NN+=1))
done
