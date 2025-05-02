import tkinter as tk
from tkinter import messagebox
import wave
import contextlib
import os

def open_cut_audio_window(input_path, output_name, output_loc, status_var, process_callback):
    window = tk.Toplevel()
    window.title("Cut Audio Configuration")
    window.geometry("300x200")
    window.resizable(False, False)

    tk.Label(window, text="Start Time (sec):").pack(pady=(10, 0))
    start_entry = tk.Entry(window)
    start_entry.pack(pady=5)

    tk.Label(window, text="End Time (sec):").pack()
    end_entry = tk.Entry(window)
    end_entry.pack(pady=5)

    # === Get duration of the selected audio file ===
    audio_file = input_path.get()
    if not os.path.exists(audio_file):
        messagebox.showerror("File Error", "Selected input audio file does not exist.")
        window.destroy()
        return

    try:
        with contextlib.closing(wave.open(audio_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
    except wave.Error:
        messagebox.showerror("Unsupported File", "This feature supports only WAV files.")
        window.destroy()
        return


    def apply_cut():
        start = start_entry.get().strip()
        end = end_entry.get().strip()

        if not (start.replace('.', '', 1).isdigit() and end.replace('.', '', 1).isdigit()):
            messagebox.showerror("Invalid Input", "Start and End times must be numbers.")
            return

        start, end = float(start), float(end)
        if start >= end:
            messagebox.showerror("Invalid Range", "End time must be greater than start time.")
            return
        
        if end > duration:
            messagebox.showerror(
                "Time Error",
                f"The end time exceeds the audio duration ({duration:.2f} seconds)."
            )
            return

        cut_settings = {"start": start, "end": end}

        window.destroy()
        process_callback(
            "Cut Audio", input_path, output_name, output_loc, status_var,
            cut_settings=cut_settings
        )

    tk.Button(window, text="Apply", command=apply_cut).pack(pady=15)