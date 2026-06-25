import streamlit as st
# import sounddevice as sd
# from scipy.io.wavfile import write
# import requests
from gtts import gTTS
from groq import Groq
import tempfile
# import shutil
import database 
import os
from streamlit_mic_recorder import mic_recorder

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

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

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

# if shutil.which("ffmpeg") is None:
#     st.error("FFmpeg not found")
#     st.stop()

#

# -------------------------
# AUDIO RECORDING
#

def record_audio(filename="input.wav"):

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        key="mic"
    )

    if not audio:
        return None
    
    audio_id = hash(audio["bytes"])
    if audio_id == st.session_state.last_audio_id:
        return None
    st.session_state.last_audio_id = audio_id

    with open(filename, "wb") as f:
        f.write(audio["bytes"])

    return filename

    



# -------------------------
# GROQ
# -------------------------



client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
# -------------------------
# STT
# -------------------------
def speech_to_text(filename="input.wav"):

    with open(filename, "rb") as file:

        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3"
        )

    return transcription.text, "en"


def ask_llama(prompt, model_name):

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


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

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        title = response.choices[0].message.content

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
    voice_reply = st.toggle(
    "🔊 Voice Reply",
    value=False
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

    

    model_name = st.selectbox(
    "Model",
    [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it"
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
if st.session_state.latest_audio:
    st.audio(st.session_state.latest_audio)


# -------------------------
# SPEAK BUTTON
# -------------------------

audio_file = record_audio()

text_input = st.chat_input(
    "Type your message..."
)

if audio_file:

    with st.spinner("🧠 Transcribing..."):

        user_text, language = speech_to_text(audio_file)

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
    
    if voice_reply:
        st.session_state.latest_audio = generate_audio(
           answer,
           language
        )
    else:
        st.session_state.latest_audio = None
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