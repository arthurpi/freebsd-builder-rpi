##
# Every setting as a default value. To use the default value, either leave a
# blank after the setting name, or comment the line

# Default value: freebsd-builder-rpi.sh
output_script_file $output_script_file

# Default value: settings.sh
output_conf_file $output_conf_file


# Default value: 128
gpu_mem $gpu_mem

# Default value: RPI-B
kern_conf $kern_conf

# Default value: /usr/src/freebsd
src_root $src_root

# Default value: /usr/obj/freebsd
obj_root $obj_root

# Default value: /mnt
mnt_dir $mnt_dir

# Default value: /usr/obj/freebsd/fbsd-rpi.img
img_name $img_name

# Default value: no
clean_obj $clean_obj

# Default value: no
do_compile $do_compile

# Default value: ./firmware
uboot_dir $uboot_dir


# Default value: pi
user $user

# Default value: raspberry
pw $pw

# Default value: 1 GB
sd_card_size $sd_card_size

# Default value: 0
img_size_raw $img_size_raw

# Default value: / full
partition_scheme $partition_scheme

# Default value: no
swap $swap

# Default value: no
disk_tune $disk_tune


# Default value: no
port_tree $port_tree

# Default value: none
pkg_prebuilt $pkg_prebuilt
