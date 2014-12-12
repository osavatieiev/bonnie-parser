#!/bin/bash
STAT_FILE="/root/bonnie/single_w1"
LOGS_DIR="/root/bonnie/c1_20_single"
#Generate Stat file
cd $LOGS_DIR; for i in `ls *.log`; do echo "${i},`tail -n1 ${i}`"; done > ${STAT_FILE}
if [ -z $1 ]
then p="*"
else p="$1"
fi
T_WR_CHR_K=0
T_WR_B_K=0
while read line
do
  LOG_FILE=`echo $line| cut -d"," -f1`
  EPOCH_DATE=`echo $line| cut -d"," -f6`
  DATE=`date -d @${EPOCH_DATE} +"%d-%m-%Y %T %z"`
  SEQ_WRITE_BLOCK_K=`echo $line| cut -d"," -f11`
  SEQ_REWRITE_K=`echo $line| cut -d"," -f13`
  SEQ_READ_CHR_K=`echo $line| cut -d"," -f15`
  SEQ_READ_BLOCK_K=`echo $line| cut -d"," -f17`
  echo "$LOG_FILE: SEQ_WRITE_BLOCK_K=${SEQ_WRITE_BLOCK_K} SEQ_REWRITE_K=${SEQ_REWRITE_K}"
  T_WR_B_K=$((T_WR_B_K+SEQ_WRITE_BLOCK_K))
  T_REWRITE_K=$((T_REWRITE_K+SEQ_REWRITE_K))
done < <(cat ${STAT_FILE}| grep "$p")
WRITE_BLOCK_G=`echo "scale=2;${T_WR_B_K}/1024/1024"|bc`
REWRITE_G=`echo "scale=2;${T_REWRITE_K}/1024/1024" | bc`
echo "TOTAL: Write_blocks=${WRITE_BLOCK_G}GB/s Rewrite=${REWRITE_G}GB/s"
