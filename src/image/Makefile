
OBJS += image.o

OBJS-$(quickdisk) += qd.o

OBJS-$(apple2) += hfe.o
OBJS-$(apple2) += mfm.o
OBJS-$(apple2) += apple2.o

ifneq ($(r8),y)
OBJS-$(shugart) += adf.o
OBJS-$(shugart) += dsk.o
endif
OBJS-$(shugart) += hfe.o
OBJS-$(shugart) += img.o
ifneq ($(r8),y)
OBJS-$(shugart) += da.o
endif
OBJS-$(shugart) += dummy.o
OBJS-$(shugart) += mfm.o
