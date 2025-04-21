import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import wave

def read_wav(file_path):
    with wave.open(file_path, "rb") as wf:
        params = wf.getparams()
        frames = wf.readframes(wf.getnframes())
    return params, frames

def write_wav(file_path, params, frames):
    with wave.open(file_path, "wb") as wf:
        wf.setparams(params)
        wf.writeframes(frames)

def ask_for_key():
    root = tk.Tk()
    root.withdraw()

    while True:
        key_option = simpledialog.askstring("Select Option", "Do you want to use a random key? (yes/no)").lower()

        if key_option == "yes":
            key = get_random_bytes(16)
            messagebox.showinfo("Generated Key", f"Random key generated: {key.hex()}")
            root.quit()  
            return key
        else:
            key_input = simpledialog.askstring("Enter Key", "Please enter the 16-byte encryption key:")
            if key_input is None or len(key_input) != 16:
                messagebox.showwarning("Invalid Key", "Key must be exactly 16 characters long!")
            else:
                root.destroy()  
                return key_input.encode()

def encrypt_audio(input_path, output_path):
    key = ask_for_key()
    if key is None:
        return  # If the key is invalid, do nothing

    params, frames = read_wav(input_path)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    encrypted = iv + cipher.encrypt(frames)
    
    write_wav(output_path, params, encrypted)

    print(f"Encrypted to {output_path} using the provided key")
