## Pre-Configured Raspberry Pi OS Lite

The file `2024-03-15-raspios-bookworm-arm64-lite.img` has been downloaded from the official [Raspberry Pi OS distribution](https://www.raspberrypi.com/software/operating-systems/#:~:text=Raspberry%20Pi%20Desktop-,Raspberry%20Pi%20OS,-Our%20recommended%20operating).

The other two files, `bcm2710-rpi-3-b.dtb` and `kernel8.img` have been extracted from it and stored as separate files.

The image has been pre-setup in order to:

- Select the QWERTY keyboard layout
- Create a user account (username and password: `rpi`)
- [Enable SSH connectivity](https://raspberrypi-guide.github.io/networking/connecting-via-ssh#:~:text=By%20default%2C%20SSH%20is%20disabled,to%20SSH%20and%20click%20OK%20.), which is turned off by default
- [Increase the storage space](https://muizidn.medium.com/increase-raspberry-pi-disk-size-in-qemu-d6d33666a930) to 8GB (from the default 2GB)
