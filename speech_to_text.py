from transformers import pipeline
from pathlib import Path
import imageio_ffmpeg
import subprocess
import numpy as np

print("Loading Whisper model...")

# Load Whisper
transcriber = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small"
)

print("Whisper is ready!")

# Locate audio file
audio_file = Path(__file__).parent / "WhatsApp Audio.ogg"

if not audio_file.exists():
    print("ERROR: WhatsApp Audio.ogg was not found!")
    print("Looking for:", audio_file)
    exit()

print("Converting audio...")

# Get FFmpeg
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

# Convert audio to raw 16 kHz mono audio
command = [
    ffmpeg,
    "-i", str(audio_file),
    "-f", "f32le",
    "-ac", "1",
    "-ar", "16000",
    "-"
]

process = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

if process.returncode != 0:
    print("ERROR: FFmpeg could not read the audio file.")
    print(process.stderr.decode(errors="ignore"))
    exit()

# Convert raw audio to NumPy
audio = np.frombuffer(
    process.stdout,
    dtype=np.float32
)

print("Audio loaded!")
print("Transcribing audio...")

# Send audio to Whisper
# Tell Whisper explicitly that the audio is English
result = transcriber(
    {
        "raw": audio,
        "sampling_rate": 16000
    },
    generate_kwargs={
        "language": "en",
        "task": "transcribe"
    }
)

# Get transcribed text
text = result["text"]

print("\n==============================")
print("YOU SAID:")
print(text)
print("==============================")

# Send text to transaction parser
from transaction_parser import parse_transaction

transaction = parse_transaction(text)
from save_transaction import save_transaction

save_transaction(transaction)

print("\n==============================")
print("NAMMAKURAL TRANSACTION")
print("==============================")

print("Type     :", transaction["type"])
print("Item     :", transaction["item"])
print("Quantity :", transaction["quantity"])
print("Unit     :", transaction["unit"])
print("Amount   : ₹", transaction["amount"])

print("==============================")