OBJS += arena.o
OBJS += build_info.o
OBJS += cancellation.o
OBJS += config.o
OBJS += crc.o
OBJS += flash_cfg.o
OBJS += vectors.o
OBJS += fpec_$(mcu).o
OBJS += fs.o
ifneq ($(r8),y)
OBJS += sd_spi.o
else
# The SELA ISR veneer in floppy.c is top-level asm referencing a static
# function, which LTO does not see.
floppy.o: CFLAGS += -fno-lto
endif
OBJS += spi.o
OBJS += string.o
OBJS += cortex.o mcu_$(mcu).o
OBJS += time.o
OBJS += timer.o
OBJS += util.o
OBJS += volume.o
OBJS-$(debug) += console.o
OBJS-$(logfile) += logfile.o

ifeq ($(target),bl_update)

OBJS += bl_update.o
SUBDIRS += display gotek

else ifeq ($(target),io_test)

OBJS += io_test.o
SUBDIRS += display gotek

else ifeq ($(target),bootloader)

OBJS += fw_update.o
SUBDIRS += display fatfs gotek usb

else

OBJS += main.o
OBJS += cache.o

OBJS-$(shugart) += floppy.o
OBJS-$(apple2) += floppy.o
OBJS-$(quickdisk) += quickdisk.o

SUBDIRS += display
SUBDIRS += fatfs
SUBDIRS += image
SUBDIRS += gotek
SUBDIRS += usb

endif

.PHONY: $(SRCDIR)/build_info.c
build_info.o: CFLAGS += -DFW_VER="\"$(FW_VER)\""

# Avoid infinite loops due to GCC noticing code that can be replaced by a call
# to a standard library function... within our implementation of that function.
util.o: CFLAGS += -fno-tree-loop-distribute-patterns

ff_cfg_defaults.h: $(ROOT)/examples/FF.CFG
	$(PYTHON) $(ROOT)/scripts/mk_config.py $< $@

main.o flash_cfg.o: ff_cfg_defaults.h
main.o flash_cfg.o: CFLAGS += -iquote .
