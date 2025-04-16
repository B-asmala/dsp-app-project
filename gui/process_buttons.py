import tkinter as tk
from tkinter import messagebox
from utils.validators import validate_inputs

def process(name, input_path, output_name, output_loc, status_var, filter_type=None):

    # the checking for valids input/output part
    if not validate_inputs(input_path, output_name, output_loc):
        return

    # message for the process update
    process_display = f"{name} ({filter_type})" if filter_type else name
    status_var.set(f"{process_display} started...")

    print(f">>> Running: {process_display} on {input_path.get()} -> {output_loc.get()}/{output_name.get()}.wav")
    
    messagebox.showinfo("Process Complete", f"{process_display} completed.")
    status_var.set("Idle")

def create_process_buttons(root, input_audio_path, output_audio_name, output_audio_location):
    frame = tk.LabelFrame(root, text="Audio Processing", padx=10, pady=10, bg="#f4f4f4")
    frame.pack(fill="x", padx=15, pady=10)

    status_var = tk.StringVar(value="Idle")
    status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor="w", bg="#e1e1e1")
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # === Create a Filter Type Selection ===
    filter_frame = tk.Frame(frame, bg="#f4f4f4")
    filter_frame.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 10))

    tk.Label(filter_frame, text="Choose Filter Type:", bg="#f4f4f4").pack(side="left")
    
    filter_choice = tk.StringVar(value="High-pass")  # Default filter
    filter_options = ["High-pass", "Low-pass", "Band-pass", "Notch"]

    filter_dropdown = tk.OptionMenu(filter_frame, filter_choice, *filter_options)
    filter_dropdown.config(width=12)
    filter_dropdown.pack(side="left", padx=5)

    # === Process Buttons ===
    processes = [
        "Noise Canceling", "Visualization", "Filter",
        "Compression", "Decompression", "Encryption",
        "Decryption", "Fourier Transform"
    ]

    # Dynamically create buttons in rows
    for index, name in enumerate(processes):
        def button_action(n=name):
            if n == "Filter":
                process(n, input_audio_path, output_audio_name, output_audio_location, status_var, filter_type=filter_choice.get())
            else:
                process(n, input_audio_path, output_audio_name, output_audio_location, status_var)

        btn = tk.Button(
            frame, text=name, width=20, height=2,
            command=button_action
        )
        btn.grid(row=(index // 3) + 1, column=index % 3, padx=10, pady=10)
