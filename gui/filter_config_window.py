# gui/filter_config_window.py
import tkinter as tk
from tkinter import ttk, messagebox

def open_filter_config(input_audio_path, output_audio_name, output_audio_location, status_var, process_callback):
    def apply_settings():
        filter_type = filter_type_var.get()
        model_type = model_type_var.get()
        order = order_var.get()
        low_freq = low_freq_var.get()
        high_freq = high_freq_var.get()

        # Basic validation
        if not filter_type:
            messagebox.showwarning("Missing Selection", "Please select a filter type.")
            return
        if model_type not in ["FIR", "IIR"]:
            messagebox.showwarning("Invalid Model", "Please select FIR or IIR.")
            return
        if not order.isdigit() or int(order) < 1:
            messagebox.showwarning("Invalid Order", "Filter order must be a positive integer.")
            return
        if filter_type in ["Low Pass", "High Pass"]:
            if not low_freq:
                messagebox.showwarning("Missing Frequency", "Please enter the cutoff frequency.")
                return
        else:  # Band or Notch
            if not low_freq or not high_freq:
                messagebox.showwarning("Missing Frequency", "Please enter both cutoff frequencies.")
                return

        config = {
            "filter_type": filter_type,
            "model_type": model_type,
            "order": int(order),
            "low_freq": float(low_freq),
            "high_freq": float(high_freq) if high_freq else None
        }

        # Pass config to the processing function
        process_callback(
            "Filter",
            input_audio_path,
            output_audio_name,
            output_audio_location,
            status_var,
            filter_settings=config
        )
        window.destroy()

    def update_fields(*args):
        # Enable/disable High Frequency field based on filter type
        if filter_type_var.get() in ["Band Pass", "Notch"]:
            high_freq_entry.config(state="normal")
        else:
            high_freq_entry.delete(0, tk.END)
            high_freq_entry.config(state="disabled")

    window = tk.Toplevel()
    window.title("Filter Configuration")
    window.geometry("350x300")
    window.resizable(False, False)

    filter_type_var = tk.StringVar()
    model_type_var = tk.StringVar(value="FIR")
    order_var = tk.StringVar()
    low_freq_var = tk.StringVar()
    high_freq_var = tk.StringVar()

    tk.Label(window, text="Filter Type:").pack(pady=5)
    filter_type_menu = ttk.Combobox(window, textvariable=filter_type_var, state="readonly")
    filter_type_menu['values'] = ["Low Pass", "High Pass", "Band Pass", "Notch"]
    filter_type_menu.pack()
    filter_type_menu.bind("<<ComboboxSelected>>", update_fields)

    tk.Label(window, text="Low Cutoff Frequency:").pack(pady=5)
    tk.Entry(window, textvariable=low_freq_var).pack()

    tk.Label(window, text="High Cutoff Frequency:").pack(pady=5)
    high_freq_entry = tk.Entry(window, textvariable=high_freq_var, state="disabled")
    high_freq_entry.pack()

    tk.Label(window, text="Filter Model (FIR / IIR):").pack(pady=5)
    model_type_menu = ttk.Combobox(window, textvariable=model_type_var, state="readonly")
    model_type_menu['values'] = ["FIR", "IIR"]
    model_type_menu.pack()

    tk.Label(window, text="Filter Order:").pack(pady=5)
    tk.Entry(window, textvariable=order_var).pack()

    tk.Button(window, text="Apply", command=apply_settings).pack(pady=10)
    tk.Button(window, text="Cancel", command=window.destroy).pack()

