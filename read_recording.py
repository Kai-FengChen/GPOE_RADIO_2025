import wave
import numpy as np

def read_wav_file(filename):
    with wave.open(filename, 'r') as wf:
        # Extract parameters
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()
        num_frames = wf.getnframes()

        print(f"Channels: {num_channels}")
        print(f"Sample Width: {sample_width} bytes")
        print(f"Frame Rate (Sample Rate): {framerate}")
        print(f"Number of Frames: {num_frames}")
        
        # Read the frames and convert to numpy array
        audio_data = wf.readframes(num_frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)  # Assuming 16-bit samples

        # Reshape for stereo audio if applicable
        if num_channels == 2:
            audio_array = audio_array.reshape(-1, 2)  # 2 channels (stereo)

    return audio_array, framerate
