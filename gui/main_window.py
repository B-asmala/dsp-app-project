import tkinter as tk
from gui.input_section import create_input_section
from gui.output_section import create_output_section
from gui.process_buttons import create_process_buttons

#                                                        --- Main GUI window ---
def launch_app():
    root = tk.Tk()
    root.title("Audio Processor")
    root.geometry("650x430")
    root.resizable(False, False)

    # Get the input path variable
    input_audio_path = create_input_section(root)

    # Get the output name and location variables
    output_audio_name, output_audio_location = create_output_section(root)

    # Pass all three to the button section
    create_process_buttons(root, input_audio_path, output_audio_name, output_audio_location)

    root.mainloop()