import sounddevice as sd
import numpy as np
import wave
import time
import logging
from datetime import datetime
import os, sys

data_directory = sys.argv[1]
# === Logging Configuration ===
script_name = "audio_recorder"
log_date = datetime.now().strftime('%Y-%m-%d')
log_filename = os.path.join(data_directory, f"{log_date}_{script_name}.log")
error_filename = os.path.join(data_directory, f"{log_date}_{script_name}_error.log")

# Create logger
logger = logging.getLogger(script_name)
logger.setLevel(logging.INFO)

# Create file and console handlers
file_handler = logging.FileHandler(log_filename)
console_handler = logging.StreamHandler()

# Define logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Separate error logger
error_logger = logging.getLogger("error_logger")
error_handler = logging.FileHandler(error_filename)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

# === Audio Configuration ===
SAMPLE_RATE = 44100  # CD-quality audio
CHANNELS = 2         # Stereo
CHUNK_SIZE = 1024    # Buffer size
RECORD_DURATION = 1 * 60  # 30 minutes in seconds

# === Recording Function ===
def record_audio():
    try:
        while True:
            # Generate new filename with date and time
            start_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = os.path.join(data_directory, f"recording_{start_time}.wav")
            logger.info(f"Starting new recording: {filename}")

            # Open WAV file for writing
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)  # 16-bit PCM
                wf.setframerate(SAMPLE_RATE)

                # Recording stream
                def callback(indata, frames, time_info, status):
                    if status:
                        logger.warning(f"Recording Status: {status}")
                    wf.writeframes(indata.tobytes())

                with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback, blocksize=CHUNK_SIZE):
                    logger.info("Recording started...")
                    time.sleep(RECORD_DURATION)  # Record for 30 minutes

    except Exception as e:
        error_logger.error(f"Recording error: {e}")

# === Start Recording ===
if __name__ == "__main__":
    logger.info("Starting continuous audio recording script.")
    record_audio()
