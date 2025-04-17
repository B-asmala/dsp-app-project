from tkinter import messagebox

# check if the input audio, output audio name/location selected or not
def validate_inputs(input_audio_path, output_audio_name, output_audio_location):
    if not input_audio_path.get():
        messagebox.showwarning("Missing Input", "Please select an input audio file first.")
        return False
    if not output_audio_name.get():
        messagebox.showwarning("Missing Output Name", "Please enter a name for the output audio.")
        return False
    if not output_audio_location.get():
        messagebox.showwarning("Missing Save Location", "Please select a location to save the output audio.")
        return False
    return True
