KERNEL_DIR=/users/jroman/OE_FR/fso-testing/tmp/work/om-gta02-angstrom-linux-gnueabi/linux-openmoko-2.6.24+r8+gitr968c41d0c32099d78927849a71e2ef3143cc05e7-r8/git/
CROSS_COMPILE=/users/jroman/OE_FR/fso-testing/tmp/cross/bin/arm-angstrom-linux-gnueabi-

make -C $KERNEL_DIR SUBDIRS=$PWD ARCH=arm modules

