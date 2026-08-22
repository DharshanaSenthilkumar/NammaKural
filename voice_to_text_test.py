import streamlit as st
from streamlit_mic_recorder import mic_recorder

from transformers import pipeline

import imageio_ffmpeg
import subprocess
import tempfile
import os
import wave

import numpy as np
import transaction_parser
from transaction_parser import parse_transaction
from save_transaction import save_transaction


# ============================================================
# PAGE CONFIG
# ============================================================
st.write("Parser file being used:")
st.code(transaction_parser.__file__)

st.set_page_config(
    page_title="NammaKural Voice Test",
    page_icon="🎤",
    layout="centered"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎤 NammaKural Voice Test")

st.write(
    "Speak a business transaction and NammaKural "
    "will convert your voice into a structured transaction."
)


# ============================================================
# LANGUAGE SELECTION
# ============================================================

st.subheader("🌐 Choose your language")

language_choice = st.selectbox(
    "What language will you speak?",
    [
        "🔄 Auto Detect",
        "🇬🇧 English",
        "🇮🇳 Tamil"
    ]
)


# ============================================================
# CONVERT LANGUAGE SELECTION
# TO WHISPER LANGUAGE CODE
# ============================================================

if language_choice == "🇬🇧 English":

    selected_language = "english"

elif language_choice == "🇮🇳 Tamil":

    selected_language = "tamil"

else:

    selected_language = None


# ============================================================
# LOAD WHISPER
# ============================================================

@st.cache_resource
def load_whisper():

    return pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small"
    )


with st.spinner("🤖 Loading NammaKural AI..."):

    whisper = load_whisper()


# ============================================================
# MICROPHONE
# ============================================================

audio = mic_recorder(

    start_prompt="🎤 Speak Transaction",

    stop_prompt="⏹️ Stop",

    just_once=True,

    use_container_width=True,

    format="wav"
)


# ============================================================
# PROCESS AUDIO
# ============================================================

if audio:

    st.success("🎤 Recording received!")


    # ========================================================
    # GET AUDIO INFORMATION
    # ========================================================

    audio_bytes = audio["bytes"]

    audio_format = audio.get("format")

    browser_sample_rate = audio.get("sample_rate")

    sample_width = audio.get("sample_width")


    st.subheader("🔍 Recording Information")

    st.write(
        "Audio format:",
        audio_format
    )

    st.write(
        "Browser sample rate:",
        browser_sample_rate
    )

    st.write(
        "Sample width:",
        sample_width
    )

    st.write(
        "Audio bytes:",
        len(audio_bytes)
    )


    # ========================================================
    # PLAY ORIGINAL AUDIO
    # ========================================================

    st.subheader("🔊 Your Recording")

    st.audio(
        audio_bytes,
        format="audio/wav"
    )


    # ========================================================
    # CREATE ORIGINAL TEMP FILE
    # ========================================================

    input_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    input_file.write(audio_bytes)

    input_file.close()


    # ========================================================
    # CREATE OUTPUT FILE
    # ========================================================

    output_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    output_file.close()


    try:

        # ====================================================
        # GET FFMPEG
        # ====================================================

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        st.write(
            "🔧 FFmpeg found successfully."
        )


        # ====================================================
        # CONVERT AUDIO
        #
        # 16 kHz
        # Mono
        # PCM 16-bit WAV
        # ====================================================

        process = subprocess.run(

            [
                ffmpeg_path,

                "-y",

                "-i",
                input_file.name,

                "-ar",
                "16000",

                "-ac",
                "1",

                "-c:a",
                "pcm_s16le",

                output_file.name
            ],

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE
        )


        # ====================================================
        # CHECK FFMPEG
        # ====================================================

        if process.returncode != 0:

            st.error(
                "❌ FFmpeg could not process the recording."
            )

            st.code(
                process.stderr.decode(
                    errors="ignore"
                )
            )

            st.stop()


        # ====================================================
        # READ WAV
        # ====================================================

        with wave.open(
            output_file.name,
            "rb"
        ) as wav_file:

            final_sample_rate = (
                wav_file.getframerate()
            )

            channels = (
                wav_file.getnchannels()
            )

            sample_width = (
                wav_file.getsampwidth()
            )

            frame_count = (
                wav_file.getnframes()
            )

            frames = wav_file.readframes(
                frame_count
            )


        # ====================================================
        # CONVERT TO NUMPY
        # ====================================================

        audio_array = np.frombuffer(
            frames,
            dtype=np.int16
        )


        # ====================================================
        # NORMALIZE
        # ====================================================

        audio_array = (

            audio_array.astype(
                np.float32
            )

            / 32768.0
        )


        # ====================================================
        # AUDIO DIAGNOSTICS
        # ====================================================

        duration = (

            len(audio_array)

            / final_sample_rate
        )


        maximum_amplitude = float(

            np.max(

                np.abs(
                    audio_array
                )
            )
        )


        average_amplitude = float(

            np.mean(

                np.abs(
                    audio_array
                )
            )
        )


        # ====================================================
        # DISPLAY DIAGNOSTICS
        # ====================================================

        st.subheader("📊 Audio Diagnostics")

        st.write(
            "Final sample rate:",
            final_sample_rate,
            "Hz"
        )

        st.write(
            "Channels:",
            channels
        )

        st.write(
            "Duration:",
            round(
                duration,
                2
            ),
            "seconds"
        )

        st.write(
            "Maximum amplitude:",
            round(
                maximum_amplitude,
                4
            )
        )

        st.write(
            "Average amplitude:",
            round(
                average_amplitude,
                4
            )
        )


        # ====================================================
        # CHECK RECORDING
        # ====================================================

        if duration < 0.5:

            st.error(
                "🚨 Recording is too short."
            )

            st.stop()


        if maximum_amplitude < 0.01:

            st.error(
                "🚨 Your recording is almost silent."
            )

            st.write(
                "The microphone is probably not "
                "capturing your voice correctly."
            )

            st.stop()


        st.success(
            "✅ Voice signal detected!"
        )


        # ====================================================
        # WHISPER TRANSCRIPTION
        # ====================================================

        st.subheader(
            "🤖 Whisper Transcription"
        )


        with st.spinner(
            "NammaKural is understanding your voice..."
        ):

            # ------------------------------------------------
            # AUTO DETECT
            # ------------------------------------------------

            if selected_language is None:

                result = whisper(

                    {
                        "raw": audio_array,

                        "sampling_rate": 16000
                    },

                    generate_kwargs={
                        "task": "transcribe"
                    }
                )


            # ------------------------------------------------
            # SPECIFIC LANGUAGE
            # ------------------------------------------------

            else:

                result = whisper(

                    {
                        "raw": audio_array,

                        "sampling_rate": 16000
                    },

                    generate_kwargs={

                        "language":
                            selected_language,

                        "task":
                            "transcribe"
                    }
                )


        # ====================================================
        # GET TEXT
        # ====================================================

        text = result["text"].strip()


        # ====================================================
        # DISPLAY TEXT
        # ====================================================

        st.subheader(
            "📝 What NammaKural heard"
        )


        if text:

            st.success(text)

        else:

            st.warning(
                "⚠️ NammaKural could not detect speech."
            )

            st.stop()


        # ====================================================
        # PARSE TRANSACTION
        # ====================================================

        st.subheader(
            "🧠 Transaction Understanding"
        )


        with st.spinner(
            "NammaKural is understanding the transaction..."
        ):

            transaction = parse_transaction(
                text
            )


        # ====================================================
        # DISPLAY STRUCTURED TRANSACTION
        # ====================================================

        st.subheader(
            "💰 NammaKural Transaction"
        )


        # ----------------------------------------------------
        # TRANSACTION TYPE
        # ----------------------------------------------------

        if transaction["type"] == "expense":

            st.write(
                "🔴 **Type:** Expense"
            )

        elif transaction["type"] == "income":

            st.write(
                "🟢 **Type:** Income"
            )

        else:

            st.write(
                "🟡 **Type:** Unknown"
            )


        # ----------------------------------------------------
        # ITEM
        # ----------------------------------------------------

        st.write(
            "🛒 **Item:**",
            transaction["item"]
            if transaction["item"]
            else "Not detected"
        )


        # ----------------------------------------------------
        # QUANTITY
        # ----------------------------------------------------

        if transaction["quantity"] is not None:

            st.write(
                "📦 **Quantity:**",
                transaction["quantity"]
            )

        else:

            st.write(
                "📦 **Quantity:** Not specified"
            )


        # ----------------------------------------------------
        # UNIT
        # ----------------------------------------------------

        if transaction["unit"]:

            st.write(
                "⚖️ **Unit:**",
                transaction["unit"]
            )

        else:

            st.write(
                "⚖️ **Unit:** Not specified"
            )


        # ----------------------------------------------------
        # AMOUNT
        # ----------------------------------------------------

        if transaction["amount"] is not None:

            st.write(
                "💰 **Amount:** ₹",
                transaction["amount"]
            )

        else:

            st.warning(
                "⚠️ Amount could not be detected."
            )


        # ====================================================
        # SAVE TO MYSQL
        # ====================================================

        st.subheader(
            "💾 Saving Transaction"
        )


        # ----------------------------------------------------
        # VALIDATION BEFORE SAVING
        # ----------------------------------------------------

        if (

            transaction["type"]
            in ["expense", "income"]

            and

            transaction["amount"]
            is not None
        ):

            with st.spinner(
                "💾 Saving transaction to NammaKural database..."
            ):

                saved = save_transaction(
                    transaction
                )


            if saved:

                st.success(
                    "✅ Transaction successfully saved to MySQL!"
                )

                st.info(
                    "🎉 Your voice transaction is now "
                    "part of the NammaKural business records."
                )

            else:

                st.error(
                    "❌ Transaction could not be saved to MySQL."
                )


        else:

            st.warning(
                "⚠️ Transaction was not saved because "
                "NammaKural could not confidently identify "
                "the transaction type and amount."
            )


        # ====================================================
        # RAW DATA
        # ====================================================

        with st.expander(
            "🔍 View parsed transaction data"
        ):

            st.json(
                transaction
            )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "❌ Something went wrong while processing audio."
        )

        st.exception(error)


    # ========================================================
    # DELETE TEMP FILES
    # ========================================================

    finally:

        if os.path.exists(
            input_file.name
        ):

            os.remove(
                input_file.name
            )


        if os.path.exists(
            output_file.name
        ):

            os.remove(
                output_file.name
            )