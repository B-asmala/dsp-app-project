import filters
import numpy as np
from scipy.io.wavfile import write

def apply_filter(input_audio_path, output_audio_name, output_audio_location, config):

  if config['filter_type'] == "Band Pass" and config['model_type'] =="FIR":
    y, Fs = filters.BandPassFIR(input_audio_path, int(config['order']), int(config['low_freq']), int(config['high_freq']))

  if config['filter_type'] == "Notch" and config['model_type'] =="FIR":
    y, Fs = filters.BandStopFIR(input_audio_path, int(config['order']), int(config['low_freq']), int(config['high_freq']))

  if config['filter_type'] == "Band Pass" and config['model_type'] =="IIR":
    y, Fs = filters.BandPassIIR(input_audio_path, int(config['order']), int(config['low_freq']), int(config['high_freq']))
  
  if config['filter_type'] == "Notch" and config['model_type'] =="IIR":
    y, Fs = filters.BandStopIIR(input_audio_path, int(config['order']), int(config['low_freq']), int(config['high_freq']))

  # Low Pass High Pass 
  if config['filter_type'] == "Low Pass" and config['model_type'] == "FIR":
    y, Fs = filters.LowPassFIR(input_audio_path, int(config['order']), int(config['low_freq']))
    
  if config['filter_type'] == "High Pass" and config['model_type'] == "FIR":
    y, Fs = filters.HighPassFIR(input_audio_path, int(config['order']), int(config['low_freq']))
    
  if config['filter_type'] == "Low Pass" and config['model_type'] == "IIR":
    y, Fs = filters.LowPassIIR(input_audio_path, int(config['order']), int(config['low_freq']))
    
  if config['filter_type'] == "High Pass" and config['model_type'] == "IIR":
    y, Fs = filters.HighPassIIR(input_audio_path, int(config['order']), int(config['low_freq']))
  
  #normalize output array signla to [-1, 1]
  y = y / np.max(np.abs(y)) 

  #convert signal to 16-bit pulse code modulation to convert it into audio .wav
  y_int16 = np.int16(y * 32767)

  #saving output audio wav file
  write(f"{output_audio_location}/{output_audio_name}.wav", Fs, y_int16)
