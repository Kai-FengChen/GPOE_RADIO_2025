import sounddevice as sd
import soundfile as sf
import queue
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

# === Recording Function ===
q = queue.Queue()
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

# === Start Recording ===
if __name__ == "__main__":
    logger.info("Starting continuous audio recording script.")
    try:
        # Generate new filename with date and time
        start_time = datetime.now()
        filename = os.path.join(data_directory, f"recording_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.wav")
        logger.info(f"Starting new recording: {filename}")
        # Make sure the file is opened before recording anything:
        with sf.SoundFile(filename, mode='x', samplerate=SAMPLE_RATE, channels=CHANNELS) as file:
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        record_duration = (datetime.now() - start_time).total_seconds()/60
        logger.info(f"Recording finished after {record_duration:.2f} minutes")
    except Exception as e:
        error_logger.error(f"Recording error: {e}")

