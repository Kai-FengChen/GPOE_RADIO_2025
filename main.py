import time
import subprocess
import os
from gpiozero import Button, LED

# GPIO Setup
BUTTON_PIN_RECORD = 27  # GPIO pin for the start/stop recording button
BUTTON_PIN_SHUTDOWN = 17  # GPIO pin for the shutdown button
LED_READY = 22             # GPIO pin for the Blue LED
LED_ACTIVE = 26            # GPIO pin for the Green LED

# Create Button and LED objects
button_record = Button(BUTTON_PIN_RECORD)
button_shutdown = Button(BUTTON_PIN_SHUTDOWN)
led_ready = LED(LED_READY)
led_active = LED(LED_ACTIVE)

# Global variable to track the background process
background_process = None
start_time = None
end_time = None
start_time_power_button = None

# Function to start the background recording script
def start_recording():
    global background_process, start_time, end_time
    if background_process is None:  # Check if a process is not already running
        print("Starting background recording script...")
        background_process = subprocess.Popen(['sudp', 'python3', '/home/gpoe/GPOE_RADIO_2025/test.py'])
        led_ready.off()
        led_active.on()  # Turn on LED to indicate recording is active

# Function to stop the background recording script
def stop_recording():
    global background_process, start_time, end_time
    if background_process is not None:
        print("Stopping background recording script...")
        background_process.terminate()  # Terminate the background process
        background_process = None
        for i in range(5):
            led_active.off()  
            time.sleep(0.1)
            led_active.on()
            # Blink LED when recording stoping
            time.sleep(0.1)
        led_active.off()
        led_ready.on()


# Toggle function for record button press
def on_button_record_press():
    if background_process is None:
        start_recording()  # Start recording if not already running
    else:
        stop_recording()   # Stop recording if already running
    time.sleep(0.1)
    
# Function to shut down the system when shutdown button is pressed
def on_button_shutdown_press():
    led_active.off()
    led_ready.off()
    print("Shutdown button pressed. Shutting down the system...")
    # os.system("sudo shutdown now")  # Shutdown the Raspberry Pi

# Handle BUTTON_SHUTDOWN press
def button_shutdown_pressed():
    global start_time_power_button
    if start_time_power_button is None:
        start_time_power_button = time.time()  # Record press time
    else:
        press_duration = time.time() - start_time_power_button
        if press_duration >= 2:
            if background_process is None:
                print(f"Shutdown button pressed for {press_duration} seconds, no recording active.")
            else:
                print(f"Shutdown button pressed for {press_duration} seconds. Stopping and saving recording.")
                stop_recording()
            time.sleep(0.1)
            led_active.off()
            led_ready.off()
            print("Shutting down the system...")

def button_shutdown_released():
    global start_time_power_button
    start_time_power_button = None  # Reset power button press time
    
# Attach the button press handlers
button_record.when_pressed = on_button_record_press
button_shutdown.when_pressed = button_shutdown_pressed
button_shutdown.when_released = button_shutdown_released

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

