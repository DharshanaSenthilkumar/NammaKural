import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

from streamlit_mic_recorder import mic_recorder
from transformers import pipeline

import imageio_ffmpeg
import subprocess
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()
import os
import wave
import numpy as np

from transaction_parser import parse_transaction


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NammaKural | AI Business Companion",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM NAMMAKURAL DESIGN
# ============================================================

st.html("""
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(139,154,83,0.13),
            transparent 25%
        ),
        radial-gradient(
            circle at 100% 0%,
            rgba(184,101,75,0.10),
            transparent 25%
        ),
        #f4f0e6;

    color: #25251f;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #29321f 0%,
            #1d2418 100%
        );

    border-right: 1px solid #59653e;
}

[data-testid="stSidebar"] * {
    color: #f5f1e8 !important;
}


/* ============================================================
   HERO
   ============================================================ */

.nk-hero {
    position: relative;
    overflow: hidden;

    padding: 38px 42px;
    margin-bottom: 28px;

    border-radius: 28px;

    background:
        linear-gradient(
            120deg,
            #303b25 0%,
            #59683b 55%,
            #8b704f 100%
        );

    box-shadow:
        0 18px 45px rgba(48,59,37,0.18);

    border: 1px solid rgba(255,255,255,0.12);
}

.nk-hero::before {
    content: "";

    position: absolute;

    width: 260px;
    height: 260px;

    right: -70px;
    top: -100px;

    border-radius: 50%;

    background:
        rgba(226,190,105,0.18);
}

.nk-hero::after {
    content: "";

    position: absolute;

    width: 130px;
    height: 130px;

    right: 170px;
    bottom: -80px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.08);
}

.nk-hero-content {
    position: relative;
    z-index: 2;
}

.nk-hero-title {
    font-size: 48px;
    font-weight: 950;
    letter-spacing: -1.5px;
    color: #fffdf7;
    margin-bottom: 5px;
}

.nk-hero-subtitle {
    font-size: 18px;
    color: #e8e5d9;
    max-width: 700px;
    line-height: 1.5;
}

.nk-ai-badge {
    display: inline-block;

    margin-top: 20px;

    padding: 8px 15px;

    border-radius: 30px;

    background:
        rgba(226,190,105,0.18);

    border:
        1px solid rgba(226,190,105,0.45);

    color: #f3d98b;

    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.4px;
}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.nk-section {
    display: flex;

    align-items: center;

    gap: 10px;

    margin-top: 30px;
    margin-bottom: 15px;

    color: #303b25;

    font-size: 25px;
    font-weight: 900;
}

.nk-description {
    color: #777763;

    font-size: 14px;

    margin-top: -8px;
    margin-bottom: 18px;
}


/* ============================================================
   VOICE CARD
   ============================================================ */

.nk-voice-card {
    background:
        linear-gradient(
            135deg,
            #303b25,
            #59683b
        );

    border-radius: 28px;

    padding: 35px;

    margin-top: 10px;
    margin-bottom: 30px;

    box-shadow:
        0 18px 40px rgba(48,59,37,0.18);

    border:
        1px solid rgba(255,255,255,0.12);

    text-align: center;
}

.nk-voice-icon {
    font-size: 72px;
    margin-bottom: 8px;
}

.nk-voice-title {
    color: #fffdf7;
    font-size: 30px;
    font-weight: 950;
}

.nk-voice-text {
    color: #e3e5d8;
    font-size: 16px;
    margin-top: 8px;
}


/* ============================================================
   KPI CARDS
   ============================================================ */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #fffdf7,
            #ece7d9
        );

    border:
        1px solid #d7d0bd;

    border-radius: 20px;

    padding: 23px;

    box-shadow:
        0 8px 25px rgba(48,59,37,0.08);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);

    box-shadow:
        0 16px 35px rgba(48,59,37,0.14);

    border-color:
        #9a9f62;
}

[data-testid="stMetricLabel"] {
    color: #74785a !important;

    font-size: 14px !important;

    font-weight: 800 !important;
}

[data-testid="stMetricValue"] {
    color: #303b25 !important;

    font-size: 30px !important;

    font-weight: 950 !important;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 12px;

    border:
        1px solid #687542;

    background:
        linear-gradient(
            135deg,
            #687542,
            #3d492d
        );

    color: white;

    font-weight: 800;

    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 22px rgba(61,73,45,0.25);
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput input,
.stNumberInput input {

    background:
        #fffdf7 !important;

    color:
        #303b25 !important;

    border:
        1px solid #c9c3b2 !important;

    border-radius:
        11px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {

    border-color:
        #8b9a53 !important;

    box-shadow:
        0 0 0 2px
        rgba(139,154,83,0.15) !important;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

.stSelectbox div[data-baseweb="select"] {

    background:
        #fffdf7 !important;

    border:
        1px solid #c9c3b2 !important;

    border-radius:
        11px !important;
}


/* ============================================================
   EXPANDER
   ============================================================ */

[data-testid="stExpander"] {

    background:
        linear-gradient(
            145deg,
            #fffdf7,
            #eee9dc
        );

    border:
        1px solid #d2cbb9;

    border-radius:
        18px;

    box-shadow:
        0 6px 20px
        rgba(48,59,37,0.07);
}


/* ============================================================
   AI CARD
   ============================================================ */

.nk-ai-card {

    background:
        linear-gradient(
            135deg,
            #303b25,
            #59683b
        );

    color:
        white;

    border-radius:
        22px;

    padding:
        25px;

    min-height:
        160px;

    box-shadow:
        0 12px 30px
        rgba(48,59,37,0.16);
}

.nk-ai-label {

    color:
        #e2be69;

    font-size:
        13px;

    font-weight:
        900;

    letter-spacing:
        1px;
}

.nk-ai-title {

    font-size:
        21px;

    font-weight:
        900;

    margin-top:
        8px;
}

.nk-ai-text {

    color:
        #e3e5d8;

    line-height:
        1.5;

    margin-top:
        8px;
}


/* ============================================================
   INSIGHT CARDS
   ============================================================ */

.nk-insight-card {

    background:
        #fffdf7;

    border:
        1px solid #d8d1bf;

    border-radius:
        20px;

    padding:
        22px;

    min-height:
        150px;

    box-shadow:
        0 8px 24px
        rgba(48,59,37,0.07);
}

.nk-insight-label {

    color:
        #74785a;

    font-size:
        13px;

    font-weight:
        900;
}

.nk-insight-value {

    color:
        #303b25;

    font-size:
        25px;

    font-weight:
        950;

    margin-top:
        10px;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

[data-testid="stDataFrame"] {

    border:
        1px solid #d2cbb9;

    border-radius:
        16px;

    overflow:
        hidden;

    box-shadow:
        0 6px 20px
        rgba(48,59,37,0.07);
}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.stDownloadButton > button {

    background:
        linear-gradient(
            135deg,
            #b8654b,
            #914a37
        );

    color:
        white;

    border:
        none;

    border-radius:
        12px;

    font-weight:
        800;
}


/* ============================================================
   FOOTER
   ============================================================ */

.nk-footer {

    text-align:
        center;

    color:
        #777763;

    padding:
        30px 0 10px;

    font-size:
        14px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 900px) {

    .nk-hero-title {
        font-size: 34px;
    }

    .nk-hero {
        padding: 28px;
    }

}

</style>
""")


# ============================================================
# MYSQL CONNECTION
# ============================================================

def get_connection():

    return mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)


# ============================================================
# LOAD WHISPER
# ============================================================

@st.cache_resource
def load_whisper():

    return pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small"
    )


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="nk-hero">

    <div class="nk-hero-content">

        <div class="nk-hero-title">
            🎤 NammaKural
        </div>

        <div class="nk-hero-subtitle">
            Your business, understood through your voice.
            Turn everyday conversations into organized
            business records and actionable insights.
        </div>

        <div class="nk-ai-badge">
            ✦ AI BUSINESS COMPANION &nbsp; • &nbsp; VOICE-FIRST
        </div>

    </div>

</div>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌿 NammaKural")

    st.caption(
        "Your everyday business companion."
    )

    st.divider()

    st.markdown("### ⚙️ Controls")

    if st.button(
        "↻ Refresh Business Data",
        use_container_width=True
    ):
        st.rerun()

    st.divider()

    st.markdown("### 🔎 Explore Transactions")

    transaction_filter = st.selectbox(
        "Transaction Type",
        [
            "All",
            "expense",
            "income"
        ]
    )

    search_item = st.text_input(
        "Search Item",
        placeholder="Try: rice, sugar..."
    )

    st.divider()

    st.markdown("### 🎤 Voice Workflow")

    st.caption(
        "Speak naturally → Whisper transcribes → "
        "AI extracts transaction details → "
        "MySQL stores your records."
    )


# ============================================================
# 🎤 VOICE TRANSACTION
# ============================================================

st.html("""
<div class="nk-section">
    🎤 Speak Your Transaction
</div>

<div class="nk-description">
    Just speak naturally. NammaKural will understand and
    record the transaction automatically.
</div>

<div class="nk-voice-card">

    <div class="nk-voice-icon">
        🎙️
    </div>

    <div class="nk-voice-title">
        Speak instead of typing
    </div>

    <div class="nk-voice-text">
        Example: "Innaiku 250 roobaikku paal vanginen"
    </div>

</div>
""")


# ============================================================
# LANGUAGE
# ============================================================

voice_language = st.selectbox(
    "🌐 Voice Language",
    [
        "🔄 Auto Detect",
        "🇬🇧 English",
        "🇮🇳 Tamil"
    ],
    key="dashboard_voice_language"
)


if voice_language == "🇬🇧 English":

    selected_language = "english"

elif voice_language == "🇮🇳 Tamil":

    selected_language = "tamil"

else:

    selected_language = None


# ============================================================
# MICROPHONE
# ============================================================

audio = mic_recorder(

    start_prompt="🎤  START SPEAKING",

    stop_prompt="⏹️  STOP RECORDING",

    just_once=True,

    use_container_width=True,

    format="wav"
)


# ============================================================
# PROCESS VOICE
# ============================================================

if audio:

    st.success(
        "🎤 Recording received!"
    )

    audio_bytes = audio["bytes"]

    st.audio(
        audio_bytes,
        format="audio/wav"
    )

    input_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    input_file.write(audio_bytes)
    input_file.close()

    output_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    output_file.close()

    try:

        # ====================================================
        # FFMPEG
        # ====================================================

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

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

            final_sample_rate = wav_file.getframerate()

            frame_count = wav_file.getnframes()

            frames = wav_file.readframes(
                frame_count
            )


        # ====================================================
        # NUMPY
        # ====================================================

        audio_array = np.frombuffer(
            frames,
            dtype=np.int16
        )

        audio_array = (
            audio_array.astype(np.float32)
            / 32768.0
        )


        duration = (
            len(audio_array)
            / final_sample_rate
        )

        maximum_amplitude = float(
            np.max(
                np.abs(audio_array)
            )
        )


        # ====================================================
        # RECORDING CHECK
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

            st.stop()


        # ====================================================
        # WHISPER
        # ====================================================

        st.subheader(
            "🤖 Understanding your voice..."
        )

        with st.spinner(
            "NammaKural is listening..."
        ):

            whisper = load_whisper()

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
        # TRANSCRIPTION
        # ====================================================

        text = result["text"].strip()


        st.subheader(
            "📝 What NammaKural heard"
        )

        if not text:

            st.warning(
                "⚠️ No speech detected."
            )

            st.stop()


        st.success(text)


        # ====================================================
        # PARSER
        # ====================================================

        st.subheader(
            "🧠 Understanding transaction..."
        )

        with st.spinner(
            "Extracting transaction details..."
        ):

            transaction = parse_transaction(
                text
            )


        # ====================================================
        # DISPLAY TRANSACTION
        # ====================================================

        st.subheader(
            "💰 NammaKural Transaction"
        )

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            if transaction["type"] == "expense":

                st.metric(
                    "Type",
                    "🔴 Expense"
                )

            elif transaction["type"] == "income":

                st.metric(
                    "Type",
                    "🟢 Income"
                )

            else:

                st.metric(
                    "Type",
                    "🟡 Unknown"
                )


        with col2:

            st.metric(
                "🛒 Item",
                transaction["item"]
                if transaction["item"]
                else "Not detected"
            )


        with col3:

            quantity_value = transaction["quantity"]

            if quantity_value:

                quantity_display = str(
                    quantity_value
                )

                if transaction["unit"]:

                    quantity_display += (
                        " "
                        + transaction["unit"]
                    )

            else:

                quantity_display = "Not specified"


            st.metric(
                "📦 Quantity",
                quantity_display
            )


        with col4:

            if transaction["amount"] is not None:

                st.metric(
                    "💰 Amount",
                    f"₹{transaction['amount']:,.0f}"
                )

            else:

                st.metric(
                    "💰 Amount",
                    "Not detected"
                )


        # ====================================================
        # SAVE TO MYSQL
        # ====================================================

        if (
            transaction["type"] in
            ["expense", "income"]
            and
            transaction["amount"] is not None
            and
            transaction["item"]
        ):

            st.subheader(
                "💾 Saving Transaction"
            )

            try:

                connection = get_connection()

                cursor = connection.cursor()

                query = """
                INSERT INTO transactions
                (type, item, quantity, unit, amount)
                VALUES
                (%s, %s, %s, %s, %s)
                """

                values = (

                    transaction["type"],

                    transaction["item"],

                    transaction["quantity"],

                    transaction["unit"],

                    transaction["amount"]
                )

                cursor.execute(
                    query,
                    values
                )

                connection.commit()

                cursor.close()

                connection.close()


                st.success(
                    "✅ Transaction successfully saved to MySQL!"
                )

                st.balloons()

                st.info(
                    "🎉 Your voice transaction is now "
                    "part of the NammaKural business records."
                )


                # =================================================
                # REFRESH DASHBOARD
                # =================================================

                st.rerun()


            except mysql.connector.Error as error:

                st.error(
                    "❌ Could not save transaction."
                )

                st.write(error)


        else:

            st.warning(
                "⚠️ Transaction was not saved because "
                "NammaKural could not confidently identify "
                "the transaction type, item, or amount."
            )


        # ====================================================
        # RAW TRANSACTION
        # ====================================================

        with st.expander(
            "🔍 View parsed transaction data"
        ):

            st.json(
                transaction
            )


    except Exception as error:

        st.error(
            "❌ Something went wrong while processing audio."
        )

        st.exception(error)


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


# ============================================================
# ADD TRANSACTION MANUALLY
# ============================================================

with st.expander(
    "＋ Add Transaction Manually"
):

    st.markdown(
        "### 🧾 Record a Business Transaction"
    )

    st.caption(
        "You can also add a transaction manually."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        transaction_type = st.selectbox(
            "Type",
            [
                "expense",
                "income"
            ],
            key="transaction_type"
        )

    with col2:

        item = st.text_input(
            "Item",
            placeholder="Example: Sugar",
            key="item"
        )

    with col3:

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0,
            key="amount"
        )

    col4, col5 = st.columns(2)

    with col4:

        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            step=1.0,
            key="quantity"
        )

    with col5:

        unit = st.text_input(
            "Unit",
            placeholder="Example: kg",
            key="unit"
        )


    if st.button(
        "💾 Save Transaction",
        type="primary",
        use_container_width=True
    ):

        if item.strip() == "":

            st.error(
                "⚠️ Please enter an item."
            )

        elif amount <= 0:

            st.error(
                "⚠️ Amount must be greater than ₹0."
            )

        else:

            try:

                connection = get_connection()

                cursor = connection.cursor()

                query = """
                INSERT INTO transactions
                (type, item, quantity, unit, amount)
                VALUES
                (%s, %s, %s, %s, %s)
                """

                cursor.execute(

                    query,

                    (
                        transaction_type,
                        item.strip(),
                        quantity,
                        unit.strip(),
                        amount
                    )
                )

                connection.commit()

                cursor.close()

                connection.close()

                st.success(
                    "✓ Transaction added to your business records."
                )

                st.rerun()

            except mysql.connector.Error as error:

                st.error(
                    "Could not save transaction."
                )

                st.write(error)


# ============================================================
# LOAD DATA
# ============================================================

try:

    connection = get_connection()

    query = """
    SELECT
        type,
        item,
        quantity,
        unit,
        amount
    FROM transactions
    """

    df = pd.read_sql(
        query,
        connection
    )

    connection.close()

except mysql.connector.Error as error:

    st.error(
        "❌ MySQL connection failed."
    )

    st.write(error)

    st.stop()


# ============================================================
# EMPTY DATABASE
# ============================================================

if df.empty:

    st.info(
        "📭 No transactions yet. "
        "Add your first business transaction."
    )

    st.stop()


# ============================================================
# CLEAN DATA
# ============================================================

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
).fillna(0)

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
).fillna(0)


# ============================================================
# FILTER
# ============================================================

filtered_df = df.copy()


if transaction_filter != "All":

    filtered_df = filtered_df[
        filtered_df["type"] ==
        transaction_filter
    ]


if search_item.strip():

    filtered_df = filtered_df[
        filtered_df["item"]
        .astype(str)
        .str.contains(
            search_item,
            case=False,
            na=False
        )
    ]


# ============================================================
# CALCULATIONS
# ============================================================

total_income = df[
    df["type"] == "income"
]["amount"].sum()


total_expenses = df[
    df["type"] == "expense"
]["amount"].sum()


balance = (
    total_income -
    total_expenses
)


total_transactions = len(df)


# ============================================================
# BUSINESS PULSE
# ============================================================

st.html("""
<div class="nk-section">
    ◈ Business Pulse
</div>

<div class="nk-description">
    A quick view of your business performance.
</div>
""")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "💰 Money In",
        f"₹{total_income:,.0f}"
    )


with col2:

    st.metric(
        "🧾 Money Out",
        f"₹{total_expenses:,.0f}"
    )


with col3:

    st.metric(
        "🌱 Current Balance",
        f"₹{balance:,.0f}"
    )


with col4:

    st.metric(
        "◉ Recorded",
        total_transactions
    )


# ============================================================
# AI BUSINESS INSIGHT
# ============================================================

expense_df = df[
    df["type"] == "expense"
]


if not expense_df.empty:

    highest_expense = (
        expense_df
        .groupby("item")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    top_item = highest_expense.index[0]

    top_amount = highest_expense.iloc[0]

    percentage = (

        top_amount /
        total_expenses *
        100

        if total_expenses > 0

        else 0
    )


    st.html("""
    <div class="nk-section">
        ✦ AI Business Insight
    </div>
    """)


    insight_text = (
        f"Your highest recorded expense is "
        f"<b>{top_item}</b> at "
        f"<b>₹{top_amount:,.0f}</b>. "
        f"This represents {percentage:.1f}% "
        f"of your total expenses."
    )


    st.html(
        f"""
        <div class="nk-ai-card">

            <div class="nk-ai-label">
                ✦ NAMMAKURAL AI
            </div>

            <div class="nk-ai-title">
                Here's something worth noticing.
            </div>

            <div class="nk-ai-text">
                {insight_text}
            </div>

        </div>
        """
    )


# ============================================================
# BUSINESS HEALTH
# ============================================================

if balance > 0:

    st.success(
        f"🌱 Positive cash position — "
        f"₹{balance:,.0f} currently recorded."
    )

elif balance < 0:

    st.error(
        f"⚠️ Expenses currently exceed "
        f"recorded income by "
        f"₹{abs(balance):,.0f}."
    )

else:

    st.warning(
        "Your recorded income and expenses are currently equal."
    )


# ============================================================
# CASH FLOW
# ============================================================

st.html("""
<div class="nk-section">
    ⌁ Cash Flow
</div>

<div class="nk-description">
    Income versus expenses across your recorded transactions.
</div>
""")


comparison_df = pd.DataFrame({

    "Category": [
        "Income",
        "Expenses"
    ],

    "Amount": [
        total_income,
        total_expenses
    ]

})


fig_cash = px.bar(

    comparison_df,

    x="Category",

    y="Amount",

    text="Amount",

    color="Category",

    color_discrete_map={

        "Income": "#718238",

        "Expenses": "#b8654b"
    }
)


fig_cash.update_traces(

    texttemplate="₹%{text:,.0f}",

    textposition="outside",

    marker_line_width=0
)


fig_cash.update_layout(

    height=420,

    showlegend=False,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font_color="#303b25",

    yaxis_title="Amount (₹)",

    xaxis_title="",

    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20
    )
)


st.plotly_chart(
    fig_cash,
    use_container_width=True
)


# ============================================================
# ANALYTICS
# ============================================================

st.html("""
<div class="nk-section">
    ◌ Business Analytics
</div>
""")


chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    st.markdown(
        "#### 🛒 Spending Pattern"
    )

    if not expense_df.empty:

        item_expenses = (
            expense_df
            .groupby("item")["amount"]
            .sum()
            .reset_index()
            .sort_values(
                "amount",
                ascending=False
            )
        )


        fig_items = px.bar(

            item_expenses,

            x="amount",

            y="item",

            orientation="h",

            text="amount",

            color="amount",

            color_continuous_scale=[

                "#d9ddc9",
                "#8b9a53",
                "#303b25"
            ]
        )


        fig_items.update_traces(

            texttemplate="₹%{text:,.0f}",

            textposition="outside"
        )


        fig_items.update_layout(

            height=450,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font_color="#303b25",

            coloraxis_showscale=False,

            xaxis_title="Amount (₹)",

            yaxis_title="",

            margin=dict(
                l=10,
                r=20,
                t=20,
                b=20
            )
        )


        st.plotly_chart(
            fig_items,
            use_container_width=True
        )

    else:

        st.info(
            "No expense data available."
        )


with chart_col2:

    st.markdown(
        "#### ◉ Expense Mix"
    )

    if not expense_df.empty:

        category_df = (
            expense_df
            .groupby("item")["amount"]
            .sum()
            .reset_index()
        )


        fig_pie = px.pie(

            category_df,

            names="item",

            values="amount",

            hole=0.58,

            color_discrete_sequence=[

                "#303b25",
                "#718238",
                "#9a9f62",
                "#b8654b",
                "#d29a83",
                "#c8cdb0"
            ]
        )


        fig_pie.update_layout(

            height=450,

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font_color="#303b25",

            margin=dict(
                l=10,
                r=10,
                t=20,
                b=20
            )
        )


        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    else:

        st.info(
            "No expense data available."
        )


# ============================================================
# QUICK INSIGHTS
# ============================================================

st.html("""
<div class="nk-section">
    ✦ What Your Numbers Say
</div>
""")


if not expense_df.empty:

    c1, c2, c3 = st.columns(3)


    with c1:

        st.html(
            f"""
            <div class="nk-insight-card">

                <div class="nk-insight-label">
                    HIGHEST EXPENSE
                </div>

                <div class="nk-insight-value">
                    {top_item}
                </div>

                <br>

                ₹{top_amount:,.0f}

            </div>
            """
        )


    with c2:

        st.html(
            f"""
            <div class="nk-insight-card">

                <div class="nk-insight-label">
                    EXPENSE CONCENTRATION
                </div>

                <div class="nk-insight-value">
                    {percentage:.1f}%
                </div>

                <br>

                of spending is on {top_item}

            </div>
            """
        )


    with c3:

        health = (
            "Healthy 🌱"
            if balance >= 0
            else "Needs attention ⚠️"
        )


        st.html(
            f"""
            <div class="nk-insight-card">

                <div class="nk-insight-label">
                    BUSINESS POSITION
                </div>

                <div class="nk-insight-value">
                    {health}
                </div>

                <br>

                Balance: ₹{balance:,.0f}

            </div>
            """
        )


# ============================================================
# TRANSACTION HISTORY
# ============================================================

st.html("""
<div class="nk-section">
    ≡ Recent Business Records
</div>
""")


if filtered_df.empty:

    st.warning(
        "No transactions match your current filters."
    )

else:

    display_df = filtered_df.copy()

    display_df.columns = [

        "Type",
        "Item",
        "Quantity",
        "Unit",
        "Amount (₹)"
    ]


    st.dataframe(

        display_df,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# EXPORT
# ============================================================

st.html("""
<div class="nk-section">
    ↓ Export
</div>
""")


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="↓ Download Business Records",

    data=csv_data,

    file_name="nammakural_transactions.csv",

    mime="text/csv",

    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="nk-footer">

    🎤 <b>NammaKural</b>

    <br><br>

    Voice → AI → Bookkeeping → Insights

    <br>

    <span style="color:#9a9f62;">
        Built for small businesses and women entrepreneurs
    </span>

</div>
""")