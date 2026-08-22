import streamlit as st
from streamlit_mic_recorder import mic_recorder


st.set_page_config(
    page_title="NammaKural Voice Test",
    page_icon="🎤"
)


st.title("🎤 NammaKural Voice Test")

st.write(
    "Press the microphone button and speak."
)


audio = mic_recorder(
    start_prompt="🎤 Speak",
    stop_prompt="⏹️ Stop",
    just_once=True,
    use_container_width=True
)


if audio:

    st.success("🎤 Audio captured successfully!")

    st.write(
        "Audio bytes received:",
        len(audio["bytes"])
    )

    st.audio(
        audio["bytes"],
        format="audio/wav"
    )