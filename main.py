import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy.signal import welch

# Function to read audio file and create DataFrame
def create_audio_dataframe(audio_file):
    # Read audio file
    sample_rate, data = wavfile.read(audio_file)
    print(f'Sample Rate: {sample_rate}')
    
    # Calculate duration of audio in seconds
    duration = len(data) / sample_rate
    
    # Time vector for DataFrame
    time = np.linspace(0., duration, len(data))
    
    # Create DataFrame
    df = pd.DataFrame({'Time': time, 'Amplitude': data})
    # df2 = df.copy()
    # for i in range(99):
    #     df = pd.concat([df, df2], ignore_index=True)
    
    return df, sample_rate

# Function to calculate the RMS value of the audio data
def calculate_rms(df):
    # Calculate squared amplitudes
    df['Amplitude_Squared'] = df['Amplitude'] ** 2
    
    # Calculate mean of squared amplitudes
    mean_squared = df['Amplitude_Squared'].mean()
    
    # Calculate RMS
    rms = np.sqrt(mean_squared)
    
    return rms

# Main function
def process_audio(audio_file):
    # Create DataFrame from audio file
    df, sample_rate = create_audio_dataframe(audio_file)
    
    # Calculate RMS
    rms_value = calculate_rms(df)
    
    print(f'RMS Value: {rms_value}')
    
    # Find points of high amplitude (above a certain threshold, e.g., RMS value)
    high_amplitude_points = df[df['Amplitude'] ** 2 > rms_value ** 2]
    
    return high_amplitude_points
high_amp_points = process_audio('eight8MBaudio.wav')
print(high_amp_points)