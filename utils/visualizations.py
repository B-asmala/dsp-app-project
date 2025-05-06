import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os

def plot_waveform(file_path, output_path='waveform.png'):
    """
    Plot and save the time-domain waveform of an audio file.
    
    Parameters:
    - file_path (str): Path to the audio file.
    - output_path (str): Path to save the waveform plot image.
    """
    y, sr = librosa.load(file_path, sr=None)
    
    plt.figure(figsize=(14, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Waveform (Time Domain)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_fft(file_path, output_path='fft_spectrum.png'):
    """
    Plot and save the frequency spectrum (FFT) of an audio file.
    
    Parameters:
    - file_path (str): Path to the audio file.
    - output_path (str): Path to save the FFT plot image.
    """
    y, sr = librosa.load(file_path, sr=None)
    
    fft = np.fft.fft(y)
    magnitude = np.abs(fft)
    frequency = np.linspace(0, sr, len(magnitude))

    plt.figure(figsize=(14, 4))
    plt.plot(frequency[:len(frequency)//2], magnitude[:len(magnitude)//2])
    plt.title('Frequency Spectrum (FFT)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
