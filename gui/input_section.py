import tkinter as tk
from tkinter import filedialog

def create_input_section(root):
    input_audio_path = tk.StringVar()

    # Input Section Frame
    frame = tk.LabelFrame(root, text="Input Audio", padx=10, pady=10, bg="#f4f4f4")
    frame.pack(fill="x", padx=15, pady=5)

    tk.Label(frame, text="Audio File:", bg="#f4f4f4").pack(side="left")
    entry = tk.Entry(frame, textvariable=input_audio_path, width=40)
    entry.pack(side="left", padx=5)
    
    # Function to take the audio file
    def browse_audio():
        path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac *.ogg")])
        if path:
            input_audio_path.set(path)

    tk.Button(frame, text="Browse", command=browse_audio).pack(side="left")

    return input_audio_path
