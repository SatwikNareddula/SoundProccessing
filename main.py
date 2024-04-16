import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.fftpack import fft
from scipy.signal import welch
import streamlit as st
import plotly.express as px

# Function to read audio file and create DataFrame
def create_audio_dataframe(audio_file):
    # Read audio file
    sample_rate, data = wavfile.read(audio_file)
    
    # Calculate duration of audio in seconds
    duration = len(data) / sample_rate
    
    # Time vector for DataFrame
    time = np.linspace(0., duration, len(data))
    
    # Create DataFrame
    df = pd.DataFrame({'Time': time, 'Amplitude': data})
    #makes the data 10MB by duplicating it 9 times and concatinating them together
    df2 = df.copy()
    for i in range(9):
        df = pd.concat([df, df2], ignore_index=True)

    print(f'Sample Rate Value: {sample_rate}')
    
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

# plotting waveform
def plot_waveform(df, rms_value):
    fig = px.line(df, x='Time', y='Amplitude', labels={'Time': 'Time (seconds)', 'Amplitude': 'Amplitude'}, title='Audio Waveform')
    # Add RMS line
    fig.add_trace(go.Scatter(x=df['Time'], y=[rms_value]*len(df['Time']), mode='lines', name='RMS', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Time'], y=[-rms_value]*len(df['Time']), mode='lines', name='-RMS', line=dict(color='red', dash='dash')))
    return fig

# Main function to process and visualize audio
def process_and_visualize_audio(audio_file):
    # Create DataFrame from audio file
    df, sample_rate = create_audio_dataframe(audio_file)
    
    # Calculate RMS
    rms_value = calculate_rms(df)
    
    st.write(f'RMS Value: {rms_value}')
    
    # Find points of high amplitude (above a certain threshold, e.g., RMS value)
    threshold = rms_value ** 2
    high_amplitude_points = df[df['Amplitude'] ** 2 > threshold]
    st.write('High Amplitude Points:', high_amplitude_points)
    
    # Plotting the waveform
    fig = plot_waveform(df, rms_value)
    st.plotly_chart(fig, use_container_width=True)

# Streamlit interface
st.title('Audio File Processor')
uploaded_file = st.file_uploader("Choose an audio file...", type=["wav"])

if uploaded_file is not None:
    process_and_visualize_audio(uploaded_file)