import time
import subprocess
import os
from gpiozero import Button, LED

# GPIO Setup
BUTTON_PIN_RECORD = 27  # GPIO pin for the start/stop recording button
BUTTON_PIN_SHUTDOWN = 17  # GPIO pin for the shutdown button
LED_READY = 22             # GPIO pin for the LED
LED_ACTIVE = 23

# Create Button and LED objects
button_record = Button(BUTTON_PIN_RECORD)
button_shutdown = Button(BUTTON_PIN_SHUTDOWN)
led_ready = LED(LED_READY)
led_active = LED(LED_ACTIVE)

# Global variable to track the background process
background_process = None

# Function to start the background recording script
def start_recording():
    global background_process
    if background_process is None:  # Check if a process is not already running
        print("Starting background recording script...")
        background_process = subprocess.Popen(['sudp', 'python3', '/home/gpoe/GPOE_RADIO_2025/test.py'])
        led_ready.off()
        led_active.on()  # Turn on LED to indicate recording is active

# Function to stop the background recording script
def stop_recording():
    global background_process
    if background_process is not None:
        print("Stopping background recording script...")
        background_process.terminate()  # Terminate the background process
        background_process = None
        led_active.off()  # Turn off LED when recording stops
        time.sleep(0.5)
        led_active.on()


# Toggle function for record button press
def on_button_record_press():
    if background_process is None:
        start_recording()  # Start recording if not already running
    else:
        stop_recording()   # Stop recording if already running

# Function to shut down the system when shutdown button is pressed
def on_button_shutdown_press():
    led_active.off()
    led_ready.off()
    print("Shutdown button pressed. Shutting down the system...")
    # os.system("sudo shutdown now")  # Shutdown the Raspberry Pi

# Attach the button press handlers
button_record.when_pressed = on_button_record_press
button_shutdown.when_pressed = on_button_shutdown_press

# Keep the script running to listen for button presses
try:
    print("Script is running... Press the buttons to control the system.")
    while True:
        time.sleep(0.1)  # Small delay to keep the script running and responsive to button presses
except KeyboardInterrupt:
    print("Script interrupted.")
finally:
    # Ensure to clean up when the script exits
    led_active.off()
    led_ready.off()
    if background_process is not None:
        background_process.terminate()  # Terminate the background process if still running

