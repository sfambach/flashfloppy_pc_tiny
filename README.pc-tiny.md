# FlashFloppy PC tiny (STM32F105R8)

A reduced build of [FlashFloppy](https://github.com/keirf/flashfloppy) that
fits the **STM32F105R8T6 (64 kB Flash)**. The stock firmware needs 128 kB
(32 kB bootloader + ~84 kB firmware + 2 kB config) and does not start on the R8.

Target: PC hosts with an SSD1306/SH1106 OLED and three buttons, e.g. the
[Mini Floppy Emulator](https://github.com/konkotgit/Mini-Floppy-Emulator).

## What is left out

| Removed | Why |
|---|---|
| Bootloader / update from USB stick | 32 kB. Flash with ST-Link or serial instead. |
| Image formats other than IMG/IMA/DSK (raw) | PC only. HFE, ADF, EDSK, D81, ST, TRD, XDF, ... are gone. |
| Host-specific raw geometries (Akai, Ensoniq, MSX, TI-99, ...) | `host = pc-dos` and the default IMG list remain. |
| HxC compatibility and indexed navigation | Native (folder) navigation only. |
| Direct-access mode (host-side selector tools) | |
| HD44780 LCD, 7-segment LED, FF OSD | OLED only. |
| Rotary encoder | Buttons only. |
| SD card | USB stick only. |
| GPT partitions on the USB stick | MBR / superfloppy only. |

`IMG.CFG` and `FF.CFG` still work; options for removed features are ignored.
The main menu hides *Update Firmware* and *Configure FF OSD* (no bootloader, no OSD).


## Configuration

Copy [examples/pc-tiny/FF.CFG](examples/pc-tiny/FF.CFG) to the root of the USB stick (FAT32) together with the .IMG/.IMA files. Set the drive-select jumper to S1.

## New blank image

Put an empty template on the stick, e.g. a 1.44 MB image of zeros
(`dd if=/dev/zero of=BLANK144.IMG bs=1024 count=1440`). On the device:
select it, open the eject menu, choose *Copy*, then *Paste*. FlashFloppy
writes a numbered copy (`BLANK144_000.IMG`, ...) next to it, which the PC
then formats. Holding SELECT for 1.5 s on a folder pastes the copy
into that folder.

## Build

```
make pc-tiny
```

Output: `out/flashfloppy-pc-tiny-r8-<ver>.hex` and `.bin`, linked at
`0x08000000`. The last 2 kB page (`0x0800F800`) holds the saved config.
The build fails if the image does not fit. It is built with LTO.

Requirements as for upstream: `gcc-arm-none-eabi`, Python 3 with `intelhex`
and `crcmod`.

## Flash

Erase the whole chip, then write the `.hex` (or the `.bin` at `0x08000000`):

- ST-Link: `openocd -f interface/stlink.cfg -f target/stm32f1x.cfg -c "program flashfloppy-pc-tiny-r8-<ver>.hex verify reset exit"`
- Serial (BOOT0 high at power-on, 3.3 V USB-TTL on PA9/PA10): `stm32flash -b 115200 -w flashfloppy-pc-tiny-r8-<ver>.hex -v /dev/ttyUSB0`
  - Verified on an STM32F105R8T6: the firmware boots, the OLED and buttons work, and a 1.44 MB image read back error-free (all 80 tracks, both sides) with a Greaseweazle. Tie BOOT0 to GND (10k), otherwise the chip may randomly start the system bootloader.
  - The bootloader locks to the first baud rate it sees after reset: after a failed attempt, reset (BOOT0 still high) before retrying. 9600 to 115200 all worked after a reset.
  - "Failed to open port": another program (e.g. the Arduino IDE) holds the port.
  - stm32flash reports "Flash: Up to 256KiB" for the whole F105/F107 family; the R8 still has 64 KB.

BOOT0 must be pulled low for normal start.

## Keeping up with upstream

All changes sit behind the make switch `r8=y` (C define `FF_R8`). Without it
the build is byte-identical to upstream, so upstream changes merge with few or
no conflicts:

```
git remote add upstream https://github.com/keirf/flashfloppy
git fetch upstream
git merge upstream/master
make pc-tiny
```

If the merged firmware no longer fits, the build stops with
`Firmware overflows by N bytes`. Headroom at the time of writing: 1140 bytes.

A monthly workflow (`.github/workflows/upstream-check.yml`) opens an issue
when upstream has new commits.

## License

As upstream: see [COPYING](COPYING).
