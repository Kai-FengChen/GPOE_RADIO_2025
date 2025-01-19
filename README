# Raspberry Pi Setup Guide

## **SETTING UP THE PI**

### **1. Download the Raspberry Pi OS onto the Micro SD card using a personal computer**
- Slide the SD card + adapter into the computer.
- Download and install the Raspberry Pi imager from [Raspberry Pi's official site](https://www.raspberrypi.com/software/).
  - Choose **Download for Windows**.
  - Allow the download to make changes to your device.
  - Go through the installation process following prompts.
- Run the **Raspberry Pi Imager**.
  - Click **Choose Device** and select the correct Raspberry Pi.
  - Click **Choose OS** and select **Raspberry Pi OS 64-bit** (or the recommended version).
  - Click **Choose Storage** and select the SDXC Card.
  - Click **Next**.
  - Click **Edit Settings**.
  - Click **Yes** to apply OS customization settings.
  - Click **Yes** to confirm writing the microSD card.
    - This process takes a few minutes.

### **2. Insert the microSD card into the Raspberry Pi and turn it on.**

### **3. For SSH Connection:**
- Open terminal on your personal computer.
- Run:
  ```sh
  ssh [username]@[hostname].local
  ```
- Enter the password.

  Alternatively, you can connect via monitor, keyboard, and mouse.

### **4. Set Up VNC Viewer for GUI Access**
- Download, install, and launch **VNC Viewer**.
- Enable VNC on the Raspberry Pi:
  - Over SSH: `sudo raspi-config > Interface options > VNC`
  - Over a monitor: Not really necessary.
- In **VNC Viewer**, enter the hostname of the VNC server: `[hostname].local`.
- Enter the username and password.

### **5. Update the System**
```sh
sudo apt-get update && sudo apt-get upgrade -y
```

### **6. Check the Installed Python Version**
```sh
python --version
```

---

## **HARDWARE WIRING**

### **Parts (Per System):**
- 2 Tactile push buttons
- 3 LEDs
- 3 Resistors (~400 ohm)
- 8 Jumper wires with sockets

### **1. Power ON/OFF Button (Button 1)**
- Wire to **GROUND (PIN 9)** and **RUN/GPIO3 (PIN 5)**.
  - Pressing the button when the Pi is off powers it on.
  - No resistors needed; RUN pin is designed for this.
- Wire to **GROUND (PIN 9)** and **GPIO17 (PIN 11)**.
  - Enable **Internal Pull-Up Resistor** in software to keep GPIO17 HIGH when the button is not pressed.
  - When Pi is on, pressing the button pulls GPIO17 to LOW and triggers shutdown.

### **2. Recording Button**
- Wire to **GROUND (PIN 14)** and **GPIO27 (PIN 13)**.
  - Enable **Internal Pull-Up Resistor** in software to keep GPIO27 HIGH when the button is not pressed.

### **3. Power ON/OFF LED (LED 1, RED)**
- Wire to **GROUND (PIN 6)** and **5V POWER (PIN 4)**.
  - **Short cathode (-) end** to **GROUND**.
  - **Long anode (+) end** through **300 OHM resistor** to **5V POWER**.
  - LED1 turns ON when the Pi is powered and OFF when it loses power.

### **4. Recording READY LED (LED 2, BLUE)**
- Wire to **GROUND (PIN 25)** and **GPIO22 (PIN 15)**.
  - **Short anode (-) end** to **GROUND**.
  - **Long cathode (+) end** through **400 OHM resistor** to **GPIO22**.
  - When GPIO22 is HIGH, LED2 is ON. When LOW, LED2 is OFF.

### **5. Recording ACTIVE LED (LED 3, GREEN)**
- Wire to **GROUND (PIN 20)** and **GPIO23 (PIN 16)**.
  - **Short anode (-) end** to **GROUND**.
  - **Long cathode (+) end** through **400 OHM resistor** to **GPIO23**.
  - When GPIO23 is HIGH, LED3 is ON. When LOW, LED3 is OFF.

---

## **BOOT SCRIPT**

### **0. Power On Indication**
- When the Pi receives power, **LED 1 (RED)** turns on.

### **1. Edit `/etc/rc.local` File**
- Open the file:
  ```sh
  sudo nano /etc/rc.local
  ```
- Before the line `exit 0`, add:
  ```sh
  /home/pi/startup.sh &
  ```
- Ensure the file is executable:
  ```sh
  sudo chmod +x /etc/rc.local
  ```

### **2. Create or Edit the Startup Script**
- Ensure it exists in `/home/pi/startup.sh`:
  ```sh
  #!/bin/bash
  python3 /home/pi/VLF_recording.py
  ```
- Make it executable:
  ```sh
  chmod +x /home/pi/startup.sh
  
