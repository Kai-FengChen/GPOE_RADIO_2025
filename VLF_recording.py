import RPi.GPIO as GPIO
import time
import os
import sounddevice as sd
import wave
from datetime import datetime

# GPIO Setup
BUTTON_POWER  = 17   # Button 1 (shutdown)
BUTTON_RECORD = 27   # Button 2 (start/stop recording)
LED_READY     = 22   # Blue, ready to record
LED_ACTIVE    = 23   # Green, recording in progress

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_POWER,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_RECORD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_READY,     GPIO.OUT)
GPIO.setup(LED_ACTIVE,    GPIO.OUT)

# Initialize the state
GPIO.output(LED_READY, GPIO.HIGH)  # Blue LED on, waiting for recording to start
GPIO.output(LED_ACTIVE, GPIO.LOW)  # Green LED off, no active recording


# Function to record audio
def record_audio(filename_left, filename_right, duration=60):  # Default duration is 1 hour (3600 seconds)
    print(f"Recording audio: {filename_left} and {filename_right}")
    os.system("touch "+filename_left)
    os.system("touch "+filename_right)
    
    fs = 44100  # Sampling frequency
    channels = 2  # Stereo (2 channels)
    start_time = time.time()  # Record start time

    # Turn on active LED and turn off ready LED
    GPIO.output(LED_READY, GPIO.LOW)
    GPIO.output(LED_ACTIVE, GPIO.HIGH)

    # Start recording for both channels (left and right)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()

    # Split channels into left and right
    left_channel = recording[:, 0]  # Left channel
    right_channel = recording[:, 1]  # Right channel

    # Save both channels as separate files
    with wave.open(filename_left, 'w') as wf_left, wave.open(filename_right, 'w') as wf_right:
        wf_left.setnchannels(1)  # Mono for left channel
        wf_left.setsampwidth(2)
        wf_left.setframerate(fs)
        wf_left.writeframes(left_channel.tobytes())

        wf_right.setnchannels(1)  # Mono for right channel
        wf_right.setsampwidth(2)
        wf_right.setframerate(fs)
        wf_right.writeframes(right_channel.tobytes())

    # Turn off active LED and turn on ready LED
    GPIO.output(LED_ACTIVE, GPIO.LOW)
    GPIO.output(LED_READY, GPIO.HIGH)



# Main Loop
try:
    counter = 0
    last_button_1_time = time.time()  # To track button 1 long press
    recording = False
    recording_start_time = 0  # To track the recording time

    while True:
        # Check for Button 2 press (start/stop recording)
        if GPIO.input(BUTTON_RECORD) == GPIO.LOW:
            # Debounce the button
            time.sleep(0.2)

            if not recording:
                # Start a new recording
                filename_left = f"~/recording_{time.strftime('%Y%m%d_%H%M%S')}_left.wav"
                filename_right = f"~/recording_{time.strftime('%Y%m%d_%H%M%S')}_right.wav"
                recording = True
                recording_start_time = time.time()
                record_audio(filename_left, filename_right)
                counter += 1
                GPIO.output(LED_ACTIVE, GPIO.HIGH)  # Green LED on for testing
                GPIO.output(LED_READY, GPIO.LOW)  # Blue LED off for testing
                time.sleep(0.1)
            else:
                # Stop the current recording
                GPIO.output(LED_ACTIVE, GPIO.LOW)  # Green LED off
                GPIO.output(LED_READY, GPIO.HIGH)  # Blue LED on
                recording = False
                os.system("touch "+filename_test+"-force_stop.wav")

        # Check for Button 1 press (shutdown)
        if GPIO.input(BUTTON_POWER) == GPIO.LOW:
            # Debounce the button
            time.sleep(0.2)

            # Check if Button 1 is pressed for more than 2 seconds
            if time.time() - last_button_1_time > 2:
                print("Shutting down...")
                if recording:
                    GPIO.output(LED_ACTIVE, GPIO.LOW)  # Green LED off
                    GPIO.output(LED_READY, GPIO.HIGH)  # Blue LED on
                    recording = False
                time.sleep(1)
                GPIO.output(LED_READY, GPIO.LOW)  # Blue LED off
                time.sleep(1)
                os.system("sudo shutdown now")
                break
            else:
                last_button_1_time = time.time()  # Reset the button press time

        # Automatically stop the recording after 1 hour
        if recording and time.time() - recording_start_time >= 65:  # 1 hour
            GPIO.output(LED_READY, GPIO.HIGH)  # Blue LED on
            for i in range(5):
                GPIO.output(LED_ACTIVE, GPIO.LOW)  # Green LED off
                time.sleep(0.1)
                GPIO.output(LED_ACTIVE, GPIO.HIGH)  # Green LED ON
                time.sleep(0.1)
            GPIO.output(LED_ACTIVE, GPIO.LOW)  # Green LED off
            recording = False

            
            recording = True
            recording_start_time = time.time()
            filename_left = f"~/recording_{time.strftime('%Y%m%d_%H%M%S')}_left.wav"
            filename_right = f"~/recording_{time.strftime('%Y%m%d_%H%M%S')}_right.wav"            
            record_audio(filename_left, filename_right)
            counter += 1
            GPIO.output(LED_ACTIVE, GPIO.HIGH)  # Green LED on for testing
            GPIO.output(LED_READY, GPIO.LOW)  # Blue LED off for testing

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

