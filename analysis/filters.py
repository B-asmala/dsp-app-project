import numpy as np
from scipy.signal import butter, firwin
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

    return b, a

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

    return b, a


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

    return b, a

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

    return b, a



#testing
#def main():
    print("IIR Band Pass Filter")
    b, a = BandPassIIR(r"C:\Users\Sandy 3Laa\Downloads\file_example_WAV_1MG.wav", 5, 1000, 3000)
    print("a",a)
    print("b",b)

    print("IIR Band Stop Filter")
    d, c = BandStopIIR(r"C:\Users\Sandy 3Laa\Downloads\file_example_WAV_1MG.wav", 5, 1000, 3000)
    print("c",c)
    print("d",d)

    print("FIR Band Pass Filter")
    f, e = BandPassFIR(r"C:\Users\Sandy 3Laa\Downloads\file_example_WAV_1MG.wav", 5, 1000, 3000)
    print("e",e)
    print("f",f)

    print("FIR Band Stop Filter")
    h, g = BandStopFIR(r"C:\Users\Sandy 3Laa\Downloads\file_example_WAV_1MG.wav", 5, 1000, 3000)
    print("g",g)
    print("h",h)
 

#if __name__ == '__main__':
    main()