import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def manual_dft(filepath, output_image='manual_dft_spectrum.png', N=2048):
    """
    Perform manual DFT on a .wav file and save the magnitude spectrum as an image.

    Parameters:
        filepath (str): Path to the input .wav file.
        output_image (str): Path to save the output image (PNG).
        N (int): Number of samples to use (must be <= total samples in file).

    Returns:
        freqs (np.ndarray): Frequencies (Hz).
        magnitude (np.ndarray): Magnitude spectrum.
    """
    # Load WAV file
    sample_rate, data = wavfile.read(filepath)

    # If stereo, take one channel
    if data.ndim > 1:
        data = data[:, 0]

    # Truncate or pad signal to N samples
    x = data[:N]

    # Manual DFT implementation
    def dft(signal):
        N = len(signal)
        result = []
        for k in range(N):
            s = 0
            for n in range(N):
                angle = 2j * np.pi * k * n / N
                s += signal[n] * np.exp(-angle)
            result.append(s)
        return np.array(result)

    X = dft(x)
    freqs = np.fft.fftfreq(len(X), d=1/sample_rate)
    magnitude = np.abs(X)

    # Plot and save
    plt.figure(figsize=(12, 6))
    plt.plot(freqs[:N//2], magnitude[:N//2])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Manual DFT Spectrum')
    plt.grid(True)
    plt.savefig(output_image, dpi=300)
    plt.close()

    # return freqs[:N//2], magnitude[:N//2]

def recursive_fft(filepath, output_image='recursive_fft_spectrum.png', N=1024):
    """
    Perform recursive Cooley-Tukey FFT on a .wav file, display and save the magnitude spectrum.

    Parameters:
        filepath (str): Path to the input .wav file.
        output_image (str): Path to save the output image (PNG).
        N (int): Number of samples to use (must be a power of 2 and <= total samples in file).

    Returns:
        freqs (np.ndarray): Frequencies (Hz).
        magnitude (np.ndarray): Magnitude spectrum.
    """
    # Load WAV file
    sample_rate, data = wavfile.read(filepath)

    # If stereo, take one channel
    if data.ndim > 1:
        data = data[:, 0]

    # Ensure data has enough samples
    x = data[:N]


    # Recursive FFT implementation
    def fft(x):
        N = len(x)
        if N <= 1:
            return x
        even = fft(x[::2])
        odd = fft(x[1::2])
        T = [np.exp(-2j * np.pi * k / N) * odd[k] for k in range(N // 2)]
        return [even[k] + T[k] for k in range(N // 2)] + \
               [even[k] - T[k] for k in range(N // 2)]

    X = fft(x)
    X = np.array(X)
    freqs = np.fft.fftfreq(N, d=1/sample_rate)
    magnitude = np.abs(X)

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(freqs[:N//2], magnitude[:N//2])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Recursive FFT Spectrum')
    plt.grid(True)
    plt.tight_layout()


    # Save the plot
    plt.savefig(output_image, dpi=300)
    plt.close()