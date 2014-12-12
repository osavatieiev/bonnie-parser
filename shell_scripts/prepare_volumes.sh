#on one of controller nodes:
source openrc
#CLEAN
nova volume-list | grep vol| awk '{print "nova volume-detach "$12" "$2}' > volume_to_detach.sh
nova volume-list | grep vol| awk '{print "nova volume-delete "$2}' > volume_to_delete.sh
sh volume_to_detach.sh
sh volume_to_delete.sh
#CREATE
#VM="akupko-rally"; for VOL_ID in `seq 1 20`; do echo "cinder create --display-name ${VM}-vol${VOL_ID} 10"; done
for VM in akupko-rally bonnie-vm1 bonnie-vm2 bonnie-vm3;
do for VOL_NAME in `seq 1 20`;
    do echo "cinder create --display-name ${VM}-vol-${VOL_NAME} 10";
    done;
done > volume_to_create.sh
sh volume_to_create.sh
#ATTACH
for VM in akupko-rally bonnie-vm1 bonnie-vm2 bonnie-vm3;
do for VOL_ID in `cinder list | grep ${VM}| awk '{print $2}'`;
    do echo "nova volume-attach ${VM} ${VOL_ID}";
    done;
done > volume_to_attach.sh
sh volume_to_attach.sh

# on each target VM
#FORMAT and MOUNT
for DISK in `lsblk | grep disk| grep -v vda| awk '{print $1}'`;
do mkfs.ext4 /dev/${DISK} && mkdir -p /mnt/${DISK} && mount /dev/${DISK} /mnt/${DISK};
done
#Verify number of mounted FileSystems
cat /proc/mounts | grep mnt | wc -l
#Run single VM tests
for VOL_ID in `seq 1 20`;
do ./run_bonnie_proc.sh ${VOL_ID};
done
#Run multiple VM tests
for i in `seq 1 20`;
do pdsh -R ssh -w 192.168.111.[73,101,99,100] "/root/bonnie/run_bonnie_proc_multiple_vm.sh ${i}";
done
