import tkinter as tk
from tkinter import filedialog

def create_output_section(root, output_audio_name=None, output_audio_location=None):
    if output_audio_name is None:
        output_audio_name = tk.StringVar()
    if output_audio_location is None:
        output_audio_location = tk.StringVar()

    # Output Section Frame
    frame = tk.LabelFrame(root, text="Output Audio", padx=10, pady=10)
    frame.pack(fill="x", padx=15, pady=5)

    tk.Label(frame, text="File Name:").pack(side="left")
    name_entry = tk.Entry(frame, textvariable=output_audio_name, width=20)
    name_entry.pack(side="left", padx=5)

    tk.Label(frame, text="Save Location:").pack(side="left")
    location_entry = tk.Entry(frame, textvariable=output_audio_location, width=20)
    location_entry.pack(side="left", padx=5)

    # Function to locate the wanted location to save the audio in
    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            output_audio_location.set(folder)

    tk.Button(frame, text="Browse", command=browse_folder).pack(side="left")

    return output_audio_name, output_audio_location
