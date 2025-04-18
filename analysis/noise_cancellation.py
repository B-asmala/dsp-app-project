import librosa
import noisereduce as nr
import soundfile as sf
import numpy as np

def auto_detect_noise(y, sr, threshold_db=-35, chunk_duration=0.2):
    """Find a low-energy segment to use as a noise sample."""
    chunk_samples = int(sr * chunk_duration)
    for i in range(0, len(y), chunk_samples):
        chunk = y[i:i + chunk_samples]
        if len(chunk) == 0:
            continue
        rms = np.sqrt(np.mean(chunk ** 2))
        db = 20 * np.log10(rms + 1e-6)
        if db < threshold_db:
            return chunk
    return y[:int(sr * 0.5)]  # fallback to first 0.5s if no quiet segment found

def apply_noise_cancellation(input_path, output_path, status_var):
    """Apply noise reduction with auto-detected noise and save the result"""
    status_var.set("Loading audio...")

    try:
        y, sr = librosa.load(input_path, sr=None)

        status_var.set("Detecting noise profile...")
        noise_sample = auto_detect_noise(y, sr)

        status_var.set("Applying noise reduction...")
        y_denoised = nr.reduce_noise(
            y=y,
            y_noise=noise_sample,
            sr=sr,
            prop_decrease=0.8,
            stationary=False,
            n_fft=2048,
            win_length=2048,
            hop_length=512,
            n_std_thresh_stationary=1.8
        )

        status_var.set("Saving output...")
        sf.write(output_path, y_denoised, sr)

        status_var.set("Done.")
        return True

    except Exception as e:
        status_var.set("Error occurred")
        print(f" Error during noise cancellation: {e}")
        return False

