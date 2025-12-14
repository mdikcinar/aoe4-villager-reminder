"""
Script to generate a simple alert sound.
Run this once to create the villager.wav file.
"""

import os
import struct
import wave
import math

def generate_beep(filename, frequency=880, duration=0.3, sample_rate=44100, volume=0.5):
    """Generate a simple beep sound and save as WAV file."""
    
    # Calculate number of samples
    num_samples = int(duration * sample_rate)
    
    # Generate samples
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        # Create a simple sine wave with fade out
        fade = 1.0 - (i / num_samples) * 0.7  # Fade out effect
        sample = math.sin(2 * math.pi * frequency * t) * volume * fade
        samples.append(int(sample * 32767))
    
    # Create second beep (higher pitch)
    for i in range(num_samples):
        t = i / sample_rate
        fade = 1.0 - (i / num_samples) * 0.7
        sample = math.sin(2 * math.pi * (frequency * 1.5) * t) * volume * fade
        samples.append(int(sample * 32767))
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        
        for sample in samples:
            wav_file.writeframes(struct.pack('<h', sample))
    
    print(f"Created: {filename}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sound_file = os.path.join(script_dir, "assets", "sounds", "villager.wav")
    generate_beep(sound_file)
    print("Sound file created successfully!")


