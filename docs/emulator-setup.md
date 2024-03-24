## Emulator Setup (Windows 10/11)

### Prerequisites:

**1. QEMU** - for emulating the Raspberry Pi environment in a PC.

**2. Git for Windows** - for running Linux commands like `ssh` and `scp` in Windows.

### 1. QEMU installation

Download and run the `.exe` installer from the [official source](https://qemu.weilnetz.de/w64/#:~:text=qemu%2Dw64%2Dsetup%2D20231224.exe).

This should add a folder `qemu` under `C:\Program Files\`, which includes `qemu-system-aarch64.exe`.

In order to run this script from anywhere, add `C:\Program Files\qemu` to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).


### 2. Git for Windows installation

Download and run the `.exe` installer from the [official source](https://gitforwindows.org/). Proceed with the default configurations.

This should add a new 'Git Bash' app to the Start menu.

### 3. Prepare files and start emulation

Download the files under `/assets/emulator` and place them in a local folder. Then, `cd` into that folder and run the following command:

```shell
qemu-system-aarch64 -machine raspi3b -cpu cortex-a53 -kernel kernel8.img -dtb bcm2710-rpi-3-b.dtb -sd 2024-03-15-raspios-bookworm-arm64-lite.img -append "root=/dev/mmcblk0p2 rw rootwait rootfstype=ext4" -m 1G -smp 4 -serial stdio -usbdevice keyboard -usbdevice mouse -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::2022-:22
```

This will launch the QEMU emulator with the same specs as the Raspberry Pi 3 Model B, and open up port 2022 for SSH connectivity.

We can then connect into it by launching Git Bash and running the command:

```shell
ssh -p 2022 rpi@localhost
```
*When prompted for a password, use 'rpi'.*

Any commands we execute on this bash terminal will now run on the emulated Raspberry Pi.

### 4. Set up Python environment

We can run a simple Python demo to test the emulated Raspberry Pi and estimate its performance when running an AI model.

In order to run the model, we'll need the model file and the corresponding Python script. Download them from `assets/demo` and place them in a local folder.

Then, `cd` into that folder and copy them to the emulator with the following command on the **Command Prompt**:

```shell
scp -P 2022 model.tflite rpi@localhost:~
scp -P 2022 run_tflite.py rpi@localhost:~
```

---

*Make sure to run the following commands **on Git Bash**, as they need to be executed inside the emulator.*

To install PIP (Python's package manager) run:

```shell
sudo apt-get -y install python3-pip
```

This allows us to install the TensorFlow Lite runtime for running the AI model:

```shell
pip install tflite-runtime --break-system-packages
```

Finally, we can run the Python script:

```shell
python3 run_tflite.py --model model.tflite
```
