import tkinter as tk
from tkinter import messagebox
from utils.validators import validate_inputs
from gui.filter_config_window import open_filter_config
import pydub
from pydub import AudioSegment
from pydub.utils import which
import os 
from analysis.noise_cancellation import apply_noise_cancellation
from utils.encrypt import encrypt_audio
from utils.decrypt import decrypt_audio
from utils.fourier_transform import manual_dft
from utils.fourier_transform import recursive_fft
from utils.visualizations import plot_fft
from utils.visualizations import plot_waveform
from gui.cut_audio_window import open_cut_audio_window

AudioSegment.converter = "/home/basmala/python/ffmpeg-git-20240629-amd64-static/ffmpeg"
pydub.utils._which = lambda name: "/home/basmala/python/ffmpeg-git-20240629-amd64-static/ffprobe" if name == "ffprobe" else which(name)


def compress_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="wav")
    audio.export(output_path, format="mp3", bitrate="64k")  

def decompress_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="mp3")
    audio.export(output_path, format="wav")

def process(name, input_path, output_name, output_loc, status_var, filter_settings=None):
    # Validate inputs first (applies for all processes)
    if not validate_inputs(input_path, output_name, output_loc):
        return

    if name == "Filter":
        print("Selected Filter Settings:", filter_settings)  # Debugging print
    elif name == "Compression":
        input_file = input_path.get()
        output_file = f"{output_loc.get()}/{output_name.get()}.mp3"
        compress_audio(input_file, output_file)
    elif name == "Decompression":
        input_file = input_path.get()
        output_file = f"{output_loc.get()}/{output_name.get()}.wav"
        decompress_audio(input_file, output_file)

    else:
        print(f"Running {name} on {input_path.get()}")

    # message for the process update
    process_display = f"{name} ({filter_settings})" if filter_settings else name
    status_var.set(f"{process_display} started...")

    print(f">>> Running: {process_display} on {input_path.get()} -> {output_loc.get()}/{output_name.get()}.wav")
    
    # Simulation of processing time (optional — add time.sleep(2) if needed)

    messagebox.showinfo("Process Complete", f"{process_display} completed.")
    status_var.set("Idle")

def create_process_buttons(root, input_audio_path, output_audio_name, output_audio_location):
    frame = tk.LabelFrame(root, text="Audio Processing", padx=10, pady=10, bg="#f4f4f4")
    frame.pack(fill="x", padx=15, pady=10)

    status_var = tk.StringVar(value="Idle")
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor="w", bg="#e1e1e1")
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # === Process Buttons ===
    processes = [
        "Noise Canceling", "Visualization", "Filter",
        "Compression", "Decompression", "Encryption",
        "Decryption", "Fourier Transform"
    ]

    # Dynamically create buttons in rows
    for index, name in enumerate(processes):
        def button_action(n=name):
            # Validate inputs first
            if not validate_inputs(input_audio_path, output_audio_name, output_audio_location):
                return

            if n == "Filter":
                # Open the filter settings window if inputs are valid
                open_filter_config(
                    input_audio_path,
                    output_audio_name,
                    output_audio_location,
                    status_var,
                    lambda *args, **kwargs: process(n, input_audio_path, output_audio_name, output_audio_location, status_var, filter_settings=kwargs.get('filter_settings'))
                )
            elif n == "Noise Canceling":
            
                output_dir = output_audio_location.get()
                output_name = output_audio_name.get()
                output_path = os.path.join(output_dir, f"{output_name}_denoised.wav")
                
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    success = apply_noise_cancellation(
                        input_audio_path.get(),
                        output_path,
                        status_var
                    )
                    if success:
                        messagebox.showinfo("Success", f"File saved to:\n{output_path}")
                    else:
                        messagebox.showerror("Error", "Failed to process audio")
                except Exception as e:
                    status_var.set("Path error")
                    messagebox.showerror("Error", f"Invalid path: {str(e)}")

            elif n == "Encryption":
                input_file = input_audio_path.get()
                output_file = os.path.join(output_audio_location.get(), f"{output_audio_name.get()}_encrypted.wav")
                try:
                    encrypt_audio(input_file, output_file)
                    messagebox.showinfo("✅Success", f"🔐Encrypted file saved to:\n{output_file}")
                except Exception as e:
                    messagebox.showerror("Encryption Error", str(e))

            elif n == "Decryption":
                input_file = input_audio_path.get()
                output_file = os.path.join(output_audio_location.get(), f"{output_audio_name.get()}_decrypted.wav")
                try:
                    decrypt_audio(input_file, output_file)
                    messagebox.showinfo("✅Success", f"🔓Decrypted file saved to:\n{output_file}")
                except Exception as e:
                    messagebox.showerror("Decryption Error", str(e))
            elif n == "Fourier Transform":
                input_file = input_audio_path.get()
                output_file = os.path.join(output_audio_location.get(), f"{output_audio_name.get()}_ft.png")
                manual_dft(input_file, output_file)
                output_file = os.path.join(output_audio_location.get(), f"{output_audio_name.get()}_cooley_turkey_ft.png")
                recursive_fft(input_file, output_file)
            elif n == "Visualization":
                input_file = input_audio_path.get()
                output_file = os.path.join(output_audio_location.get(), f"{output_audio_name.get()}_time.png")
                plot_waveform(input_file, output_file)
                input_file = input_audio_path.get()
                output_file = os.path.join(output_audio_location.get(), f"{output_audio_name.get()}_freq.png")
                plot_fft(input_file, output_file)

        btn = tk.Button(
            frame, text=name, width=20, height=2,
            command=button_action
        )
        btn.grid(row=(index // 3) + 1, column=index % 3, padx=10, pady=10)

