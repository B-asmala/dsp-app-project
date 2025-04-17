import numpy as np
from scipy.signal import butter, firwin, lfilter
from scipy.io import wavfile



###############Finite Impulse Response Filters###############

#FIR Band Pass filter function, it takes the audio path .wav, n(filter order), cutoff freqs(lowCutFreq,highCutFreq)
def BandPassFIR(audio_path,n,lowCutFreq,highCutFreq):
    
    #extracting sampling frequency & signal array from audio
    Fs , x = wavfile.read(audio_path)

    #samples no. of signal is same as siganl array length
    N = len(x)

    #calculating signal time
    time = N/Fs

    #discretizing time (required for plotting)
    t = np.linspace(0, time, N)
    
    #Designing FIR band path filter using firwin function to get filter equation
    a = 1 
    b = firwin(n, [lowCutFreq, highCutFreq], pass_zero=False, fs=Fs) #pass_zero=False for bandpass filter

    #generating output signal after filtering
    y = lfilter(b, a, x)    

    
    return y, Fs

#FIR Band Stop filter function, it takes the audio path .wav, n(filter order), cutoff freqs(lowCutFreq,highCutFreq)
def BandStopFIR(audio_path,n,lowCutFreq,highCutFreq):
    
    #extracting sampling frequency & signal array from audio
    Fs , x = wavfile.read(audio_path)

    #samples no. of signal is same as siganl array length
    N = len(x)

    #calculating signal time
    time = N/Fs

    #discretizing time (required for plotting)
    t = np.linspace(0, time, N)

    #Designing FIR notch filter using firwin function to get filter equation
    a = 1 
    b = firwin(n, [lowCutFreq, highCutFreq], pass_zero=True, fs=Fs) #pass_zero=True for bandpass filter

    #generating output signal after filtering
    y = lfilter(b, a, x)
    
    return y, Fs


###############Infinite Impulse Response Filters###############

#IIR Band Pass filter function, it takes the audio path .wav, n(filter order), cutoff freqs(lowCutFreq,highCutFreq)
def BandPassIIR(audio_path,n,lowCutFreq,highCutFreq):
    
    #extracting sampling frequency & signal array from audio
    Fs , x = wavfile.read(audio_path)

    #samples no. of signal is same as siganl array length
    N = len(x)

    #calculating signal time
    time = N/Fs

    #discretizing time (required for plotting)
    t = np.linspace(0, time, N)
    
    low = lowCutFreq/(Fs/2)
    high = highCutFreq/(Fs/2)

    #Designing IIR band path filter using butter function to get filter equation
    b, a = butter(n, [low, high], btype='bandpass')

    #generating output signal after filtering
    y = lfilter(b, a, x)
    
    return y, Fs

#IIR Band Stop filter function, it takes the audio path .wav, n(filter order), cutoff freqs(lowCutFreq,highCutFreq)
def BandStopIIR(audio_path,n,lowCutFreq,highCutFreq):
    
    #extracting sampling frequency & signal array from audio
    Fs , x = wavfile.read(audio_path)

    #samples no. of signal is same as siganl array length
    N = len(x)

    #calculating signal time
    time = N/Fs

    #discretizing time (required for plotting)
    t = np.linspace(0, time, N)
    
    low = lowCutFreq/(Fs/2)
    high = highCutFreq/(Fs/2)

    #Designing IIR notch filter using butter function to get filter equation
    b, a = butter(n, [low, high], btype='bandstop')

    #generating output signal after filtering
    y = lfilter(b, a, x)
    
    return y, Fs
