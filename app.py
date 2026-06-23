import streamlit as st
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import requests
from gtts import gTTS
import tempfile
import shutil
import database 
import os

print(dir(database))
print("DB PATH:", os.path.abspath(database.DB_NAME))

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Voice AI Copilot",
    page_icon="🎤",
    layout="wide"
)
if "latest_audio" not in st.session_state:
    st.session_state.latest_audio = None
# -------------------------
# DB INIT
# -------------------------

database.init_db()

# create first chat if none exist

if len(database.get_chats()) == 0:
    database.create_chat("New Chat")

# -------------------------
# FFMPEG CHECK
# -------------------------

if shutil.which("ffmpeg") is None:
    st.error("FFmpeg not found")
    st.stop()

# -------------------------
# WHISPER
# -------------------------

@st.cache_resource
def load_model():
    return whisper.load_model("base")

MODEL = load_model()

# -------------------------
# AUDIO RECORDING
# -------------------------

def record_audio(
        filename="input.wav",
        duration=5,
        fs=44100):

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, fs, recording)

# -------------------------
# STT
# -------------------------

def speech_to_text(filename="input.wav"):

    result = MODEL.transcribe(filename)

    return result["text"], result["language"]

# -------------------------
# OLLAMA
# -------------------------

def ask_llama(prompt, model_name):

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

def generate_chat_title(user_text, model_name):

    prompt = f"""
    Create a short title for this conversation.

    Rules:
    - Maximum 5 words
    - No quotation marks
    - Return only the title

    User message:
    {user_text}
    """

    try:

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        title = response.json()["response"]

        title = title.replace('"', "")
        title = title.replace("\n", "")

        return title[:50]

    except:
        return "New Chat"

# -------------------------
# TTS
# -------------------------

def generate_audio(text, language):


    

    if language == "as":
        language = "bn"

    try:
        tts = gTTS(
            text=text,
            lang=language
        )
    except:
        tts = gTTS(
            text=text,
            lang="en"
        )

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_file.name)
    

    return temp_file.name

# -------------------------
# SIDEBAR
# -------------------------

with st.sidebar:

    st.header("💬 Chats")

    if st.button("➕ New Chat"):

        database.create_chat(
            f"Chat {len(database.get_chats()) + 1}"
        )

        st.rerun()

    chats = database.get_chats()

    chat_titles = [title for chat_id, title in chats]

    selected_chat = st.radio(
        "Select Chat",
        chat_titles
    )

    current_chat_id = next(
        chat_id
        for chat_id, title in chats
        if title == selected_chat
    )

    st.divider()

    st.subheader("✏️ Rename Chat")

    new_title = st.text_input(
        "Chat Name",
        value=selected_chat
    )

    if st.button("💾 Save Name"):

        if new_title.strip():

            database.rename_chat(
                current_chat_id,
                new_title.strip()
            )

            st.success("Chat renamed!")

            st.rerun()

    st.divider()

    duration = st.slider(
        "Recording Duration",
        3,
        15,
        5
    )

    model_name = st.selectbox(
    "Model",
    [
        "llama3",
        "mistral",
        "phi3"
    ]
)
    if st.button(
    "🗑 Delete Current Chat",
    use_container_width=True
    ):

        st.write("Deleting:", current_chat_id)

        database.delete_chat(current_chat_id)

        st.write("After delete:")
        st.write(database.get_chats())

        st.stop()

# -------------------------
# HEADER
# -------------------------

st.title("🎤 Multilingual Voice AI Copilot")

# -------------------------
# LOAD MESSAGES
# -------------------------

messages = database.get_messages(
    current_chat_id
)

for role, content in messages:

    with st.chat_message(role):
        st.write(content)

# -------------------------
# SPEAK BUTTON
# -------------------------

record = st.button(
    "🎤 Speak",
    use_container_width=True
)
text_input = st.chat_input(
    "Type your message..."
)

if record:

    with st.spinner("🎤 Listening..."):
        record_audio(duration=duration)

    with st.spinner("🧠 Transcribing..."):
        user_text, language = speech_to_text()

    st.info(f"🎙️ Detected: {user_text}")

elif text_input:

    user_text = text_input
    language = "en"

else:
    user_text = None

if user_text:

    # -------------------------
    # BUILD MEMORY
    # -------------------------

    history = ""

    old_messages = database.get_messages(
        current_chat_id
    )

    for role, content in old_messages:

        if role == "user":
            history += f"User: {content}\n"
        else:
            history += f"Assistant: {content}\n"

    prompt = f"""
You are a helpful multilingual AI assistant.

Rules:
- Answer only the latest user question.
- Use previous messages only as context.
- Be factual and concise.
- Do not roleplay unless explicitly asked.

Conversation:
{history}

User: {user_text}

Assistant:
"""

    with st.spinner("🤖 Thinking..."):

        answer = ask_llama(
            prompt,
            model_name
        )

    # Save messages

    database.save_message(
        current_chat_id,
        "user",
        user_text
    )

    database.save_message(
        current_chat_id,
        "assistant",
        answer
    )

    # Generate audio

    st.session_state.latest_audio = generate_audio(
        answer,
        language
    )

    # Auto title

    current_messages = database.get_messages(
        current_chat_id
    )

    if (
        selected_chat.startswith("Chat")
        or selected_chat == "New Chat"
    ) and len(current_messages) <= 2:

        generated_title = generate_chat_title(
            user_text,
            model_name
        )

        database.rename_chat(
            current_chat_id,
            generated_title
        )

    st.rerun()