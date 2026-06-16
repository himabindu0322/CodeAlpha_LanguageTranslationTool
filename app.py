import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pyperclip
import io

st.set_page_config(
    page_title="Language Translation Tool",
    page_icon="🌐",
    layout="centered"
)

# Professional CSS
st.markdown("""
<style>

/* Main app background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e293b 50%,
        #334155 100%
    );
    color: white;
}

/* Title */
h1 {
    text-align: center;
    color: #38bdf8 !important;
    font-size: 42px !important;
}

/* Subtext */
p {
    color: #e2e8f0 !important;
    font-size: 17px;
}

/* Text areas */
textarea {
    border-radius: 15px !important;
    border: 2px solid #38bdf8 !important;
}

/* Select boxes */
.stSelectbox > div > div {
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    ) !important;

    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    height: 50px !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

.stButton > button:hover {
    transform: scale(1.03);
    transition: 0.3s;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1e293b;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-size: 18px !important;
    font-weight: bold !important;
}

/* Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


st.title("🌐 AI Language Translation Tool")
st.write("Translate text into multiple languages with Text-to-Speech.")

# Initialize translation history
if "history" not in st.session_state:
    st.session_state.history = []

# Language dictionary
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Arabic": "ar"
}

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

text = st.text_area(
    "✍ Enter Text",
    height=180,
    placeholder="Type your text here..."
)

translated = ""

if st.button("🔄 Translate", use_container_width=True):

    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            translated = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            ).translate(text)

            st.success("✅ Translation Completed")

            st.text_area(
                "🌍 Translated Text",
                value=translated,
                height=180
            )

            # Save to history
            st.session_state.history.insert(0, {
                "source_lang": source,
                "target_lang": target,
                "original": text,
                "translated": translated
            })

            # Copy button
            if st.button("📋 Copy Translation"):
                pyperclip.copy(translated)
                st.toast("Copied to clipboard!")

            # Text-to-Speech
            st.subheader("🔊 Listen to Translation")

            tts = gTTS(
                text=translated,
                lang=languages[target].split("-")[0]
            )

            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)

            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="⬇ Download Audio",
                data=audio_bytes,
                file_name="translation.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# Sidebar History
st.sidebar.header("📜 Translation History")

if st.sidebar.button("🗑 Clear History"):
    st.session_state.history = []
    st.sidebar.success("History Cleared!")

if len(st.session_state.history) == 0:
    st.sidebar.write("No translations yet.")
else:
    for i, item in enumerate(st.session_state.history, start=1):
        with st.sidebar.expander(f"Translation {i}"):
            st.write(f"**From:** {item['source_lang']}")
            st.write(f"**To:** {item['target_lang']}")
            st.write("**Original:**")
            st.write(item["original"])
            st.write("**Translated:**")
            st.write(item["translated"])

st.markdown("---")
st.caption("Developed for CodeAlpha AI Internship 🚀")
