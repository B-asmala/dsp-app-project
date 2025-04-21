import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from Crypto.Cipher import AES
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
        key_input = simpledialog.askstring("Enter Key", "Please enter the 16-byte decryption key:")
        
        if key_input is None or len(key_input) != 16:
            messagebox.showwarning("Invalid Key", "Key must be exactly 16 characters long!")
        else:
            root.destroy()  
            return key_input.encode()

def decrypt_audio(input_path, output_path):
    key = ask_for_key()
    if key is None:
        return

    params, frames = read_wav(input_path)
    iv = frames[:16]
    encrypted = frames[16:]

    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    decrypted = cipher.decrypt(encrypted)
    
    write_wav(output_path, params, decrypted)

    print(f"Decrypted to {output_path} using the provided key")
