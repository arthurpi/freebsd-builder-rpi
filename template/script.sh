#!/bin/sh

# Abort when a command fails
set -e

# Settings
export GPU_MEM=$gpu_mem # ok
export KERN_CONF=$kern_conf
export SRC_ROOT=$src_root
export OBJ_ROOT=$obj_root
export MNT_DIR=$mnt_dir
export IMG_NAME=$img_name
export DO_COMPILE=$do_compile
export CLEAN_OBJ=$clean_obj



export MAKEOBJDIRPREFIX=$obj_root


export USER_NAME=$user
export USER_PASSWORD=$pw

## ADD PARTITION DETAILS HERE

export PORT_TREE=$port_tree
export PKG_PREBUILT=$pkg_prebuilt

export UBOOT_DIR=$uboot_dir

export TARGET_ARCH=armv6
export MAKESYSPATH=$SRC_ROOT/share/mk
# End Settings

if [ $(whoami) != "root" ]; then
  echo "This script must be executed as root. Abort..."
  exit 1
fi

if [ -z "$MNT_DIR" ]; then
  echo "MNT_DIR is not set properly. Aborting..."
  exit 1
fi

KERNEL=`realpath $OBJ_ROOT`/arm.armv6/`realpath $SRC_ROOT`/sys/$KERN_CONF/kernel
UBLDR=`realpath $OBJ_ROOT`/arm.armv6/`realpath $SRC_ROOT`/sys/boot/arm/uboot/ubldr
DTB=`realpath $OBJ_ROOT`/arm.armv6/`realpath $SRC_ROOT`/sys/$KERN_CONF/rpi.dtb

if [ $DO_COMPILE = "yes" ]; then
  if [ $CLEAN_OBJ = "no" ]; then
    export OPTS="-DNO_CLEAN"
  fi
  make -C $SRC_ROOT $OPTS kernel-toolchain
  make -C $SRC_ROOT $OPTS KERNCONF=$KERN_CONF WITH_FDT=yes buildkernel
  make -C $SRC_ROOT $OPTS MALLOC_PRODUCTION=yes buildworld
fi

buildenv=`make -C $SRC_ROOT buildenvvars`

eval $buildenv make -C $SRC_ROOT/sys/boot clean
eval $buildenv make -C $SRC_ROOT/sys/boot obj
eval $buildenv make -C $SRC_ROOT/sys/boot UBLDR_LOADADDR=0x2000000 all

rm -f $IMG_NAME

# Include image size data
dd if=/dev/zero of=$IMG_NAME bs=128M count=8
MDFILE=`mdconfig -a -f $IMG_NAME`
gpart create -s MBR ${MDFILE}

# Boot partition
gpart add -s 32m -t '!12' ${MDFILE}
gpart set -a active -i 1 ${MDFILE}
newfs_msdos -L boot -F 16 /dev/${MDFILE}s1
mount_msdosfs /dev/${MDFILE}s1 $MNT_DIR

cp $UBOOT_DIR/* $MNT_DIR
#fetch -q -o - http://people.freebsd.org/~gonzo/arm/rpi/freebsd-uboot-20130201.tar.gz | tar -x -v -z -C $MNT_DIR -f -

cat >> $MNT_DIR/CONFIG.TXT<<__EOC__
gpu_mem=$GPU_MEM
device_tree=devtree.dat
device_tree_address=0x100
disable_commandline_tags=1
__EOC__

cp $UBLDR $MNT_DIR
if [ ! -f $DTB ]; then
  echo "DTB missing, doing it manually"
  dtc -O dtb -o $DTB 0 -p 1024 `realpath $SRC_ROOT`/sys/boot/fdt/dts/rpi.dts
else
  echo "DTB already present"
fi
cp $DTB $MNT_DIR/devtree.dat
umount $MNT_DIR

# FreeBSD partition
## Custom optional
gpart add -t freebsd ${MDFILE}
gpart create -s BSD ${MDFILE}s2
gpart add -t freebsd-ufs ${MDFILE}s2
newfs /dev/${MDFILE}s2a

# Turn on Softupdates
tunefs -n enable /dev/${MDFILE}s2a
# Turn on SUJ with a minimally-sized journal.
# This makes reboots tolerable if you just pull power on the BB
# Note:  A slow SDHC reads about 1MB/s, so a 30MB
# journal can delay boot by 30s.
tunefs -j enable -S 4194304 /dev/${MDFILE}s2a
# Turn on NFSv4 ACLs
tunefs -N enable /dev/${MDFILE}s2a

mount /dev/${MDFILE}s2a $MNT_DIR

make -C $SRC_ROOT DESTDIR=$MNT_DIR -DDB_FROM_SRC installkernel
make -C $SRC_ROOT DESTDIR=$MNT_DIR -DDB_FROM_SRC installworld
make -C $SRC_ROOT DESTDIR=$MNT_DIR -DDB_FROM_SRC distribution

echo 'fdt addr 0x100' > $MNT_DIR/boot/loader.rc

echo '/dev/mmcsd0s2a / ufs rw,noatime 1 1' > $MNT_DIR/etc/fstab

cat > $MNT_DIR/etc/rc.conf <<__EORC__
hostname="raspberry-pi"
ifconfig_ue0="DHCP"
sshd_enable="YES"

devd_enable="YES"
sendmail_submit_enable="NO"
sendmail_outbound_enable="NO"
sendmail_msp_queue_enable="NO"
__EORC__

cat > $MNT_DIR/etc/ttys <<__EOTTYS__
ttyv0 "/usr/libexec/getty Pc" xterm on secure
ttyv1 "/usr/libexec/getty Pc" xterm on secure
ttyv2 "/usr/libexec/getty Pc" xterm on secure
ttyv3 "/usr/libexec/getty Pc" xterm on secure
ttyv4 "/usr/libexec/getty Pc" xterm on secure
ttyv5 "/usr/libexec/getty Pc" xterm on secure
ttyv6 "/usr/libexec/getty Pc" xterm on secure
ttyu0 "/usr/libexec/getty 3wire.115200" dialup on secure
__EOTTYS__

echo $USER_PASSWORD | pw -V $MNT_DIR/etc useradd -h 0 -n $USER_NAME -c "Raspberry Pi User" -s /bin/csh -m
pw -V $MNT_DIR/etc groupmod wheel -m $USER_NAME
USER_UID=`pw -V $MNT_DIR/etc usershow $USER_NAME | cut -f 3 -d :`
USER_GID=`pw -V $MNT_DIR/etc usershow $USER_NAME | cut -f 4 -d :`
mkdir -p $MNT_DIR/home/$USER_NAME
chown $USER_UID:$USER_GID $MNT_DIR/home/$USER_NAME

umount $MNT_DIR
mdconfig -d -u $MDFILE
