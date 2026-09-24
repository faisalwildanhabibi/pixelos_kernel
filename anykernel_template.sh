### AnyKernel3 Ramdisk Mod Script
### Poco F3 (alioth / aliothin) - Pure Kernel Installer for PixelOS / AOSP / Custom ROMs

## AnyKernel setup
# begin properties
properties() { '
kernel.string=APTKernel Pure for Poco F3 (alioth)
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=alioth
device.name2=aliothin
supported.versions=
'; } # end properties

# shell variables
BLOCK=boot;
IS_SLOT_DEVICE=auto;
RAMDISK_COMPRESSION=auto;

block=boot;
is_slot_device=auto;
ramdisk_compression=auto;

## AnyKernel methods (DO NOT CHANGE)
# import patching functions/variables - see for reference
. tools/ak3-core.sh;

## AnyKernel file attributes
set_perm_recursive 0 0 750 750 $ramdisk/* 2>/dev/null;

## AnyKernel install
dump_boot;

# Pure kernel: preserve ramdisk completely, no dtbo, no dtb override
write_boot;
## end install
