import time
import subprocess
import os
from gpiozero import Button, LED
import logging
from datetime import datetime

# Logging
script_name = "GPOE_radio_recording"
log_date = datetime.now().strftime('%Y-%m-%d')
log_filename = f"{script_name}-{log_date}.log"
error_filename = f"{script_name}-{log_date}_error.log"

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

error_logger = logging.getLogger("error_logger")
error_handler = logging.FileHandler(error_filename)
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
error_handler.setFormatter(error_formatter)
error_logger.addHandler(error_handler)

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
SCRIPT_PATH = '/home/gpoe/GPOE_RADIO_2025/audio_recording.py'

# Function to start the background recording script
def start_recording():
    global background_process, start_time, end_time
    try:
        if background_process is None:  # Check if a process is not already running
            logging.info("Starting background recording script...")
            background_process = subprocess.Popen(['sudo', 'python3', SCRIPT_PATH])
            led_ready.off()
            led_active.on()  # Turn on LED to indicate recording is active
        else:
            logging.info("Recording already in progress.")
    except Exception as e:
        error_logger.error(f"Error in start_recording: {e}")
        
# Function to stop the background recording script
def stop_recording():
    global background_process, start_time, end_time
    try:
        if background_process is not None:
            logging.info("Stopping background recording script...")
            background_process.terminate()  # Terminate the background process
            background_process.wait()  # Ensure proper process termination
            background_process = None
            led_active.blink(on_time=0.1, off_time=0.1, n=5, background=False)  # Blink LED 5 times
            led_active.off()
            led_ready.on()
        else:
            logging.info("No recording to stop.")
    except Exception as e:
        error_logger.error(f"Error in stop_recording: {e}")

        
# Toggle function for record button press
def on_button_record_press():
    try:
        if background_process is None:
            start_recording()
        else:
            stop_recording()
        time.sleep(0.1)
    except Exception as e:
        error_logger.error(f"Error in on_button_record_press: {e}")
        
# Handle BUTTON_SHUTDOWN press
def button_shutdown_pressed():
    global start_time_power_button
    start_time_power_button = time.time()  # Record press time

def button_shutdown_released():
    global start_time_power_button    
    press_duration = time.time() - start_time_power_button
    if press_duration >= 2:
        if background_process is None:
            logging.info(f"Shutdown button held for {press_duration:.2f} seconds. No recording in progress..")
        else:
            logging.info(f"Shutdown button held for {press_duration:.2f} seconds. Stopping recording before shutdown.")
            stop_recording()
        time.sleep(0.1)
        logging.info("Shutting down the system...")        
        led_active.off()
        led_ready.off()

    else:
        start_time_power_button = None  # Reset power button press time
    
# Attach the button press handlers
button_record.when_pressed = on_button_record_press
button_shutdown.when_pressed = button_shutdown_pressed
button_shutdown.when_released = button_shutdown_released

# Main loop
try:
    logging.info("Script is running... Press the buttons to control the system.")
    led_ready.on()
    while True:
        time.sleep(0.1)  # Keep script running
except KeyboardInterrupt:
    logging.info("Script interrupted.")
except Exception as e:
    error_logger.error(f"Unexpected error in main loop: {e}")
finally:
    logging.info("Cleaning up GPIO and terminating processes.")
    led_active.off()
    led_ready.off()
    if background_process is not None:
        stop_recording()
