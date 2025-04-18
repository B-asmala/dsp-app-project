import tkinter as tk
from tkinter import messagebox
from utils.validators import validate_inputs
from gui.filter_config_window import open_filter_config
from pydub import AudioSegment
import os 
from analysis.noise_cancellation import apply_noise_cancellation

def compress_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path, format="wav")
    audio.export(output_path, format="mp3", bitrate="64k")  

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



        btn = tk.Button(
            frame, text=name, width=20, height=2,
            command=button_action
        )
        btn.grid(row=(index // 3) + 1, column=index % 3, padx=10, pady=10)

