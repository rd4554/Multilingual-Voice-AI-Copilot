# 🎤 Multilingual Voice AI Copilot

A powerful Multilingual Voice Assistant built using Streamlit, Groq LLMs, Whisper Speech-to-Text, Google Text-to-Speech, and SQLite.

The application allows users to interact with AI using either voice or text, maintain multiple chat sessions, generate AI-powered responses, and optionally receive spoken replies.

---

## 🚀 Features

### 🎙️ Voice Input
- Record audio directly from the browser.
- Uses Groq Whisper Large V3 for Speech-to-Text (STT).
- Automatically transcribes user speech.

### 💬 Text Chat
- Chat with the AI using text input.
- Works seamlessly alongside voice interactions.

### 🤖 Multiple AI Models
Choose from:

- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- gemma2-9b-it

Powered by the Groq API for ultra-fast inference.

### 🧠 Conversation Memory
- Stores previous messages.
- Uses chat history as context for future responses.

### 📂 Multi-Chat Management
- Create new chats.
- Rename chats.
- Delete chats.
- Switch between conversations.

### 🔊 Voice Replies
- Convert AI responses into speech using Google Text-to-Speech (gTTS).
- Optional voice response toggle.

### 🏷️ Auto Chat Titles
- Automatically generates chat titles based on the first user message.

### 💾 Persistent Storage
- Uses SQLite for storing chats and messages.
- Data remains available after restarting the application.

### 🌍 Multilingual Support
Supports multiple languages through Whisper and gTTS, including:

- English
- Hindi
- Assamese
- Bengali
- Many more

---

# 🏗️ Tech Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| LLM | Groq API |
| Speech-to-Text | Whisper Large V3 |
| Text-to-Speech | gTTS |
| Database | SQLite |
| Voice Recording | streamlit-mic-recorder |

---

# 📁 Project Structure

```text
project/
│
├── app.py
├── database.py
├── chat.db
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/voice-ai-copilot.git

cd voice-ai-copilot
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

Create a file named `requirements.txt`

```text
streamlit
groq
gtts
streamlit-mic-recorder
```

Install:

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure Groq API Key

Create the following file:

```text
.streamlit/secrets.toml
```

Add your API key:

```toml
GROQ_API_KEY = "your_groq_api_key"
```

Get your API key from:

https://console.groq.com

---

# ▶️ Running the Application

Start the Streamlit server:

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

---
## 🌐 Live Demo

Try the deployed application here:

🔗 https://multilingual-voice-ai-copilot-rd.streamlit.app/

### Features Available on Live Demo

- 🎤 Voice Recording
- 💬 Text Chat
- 🤖 Multiple AI Models
- 🧠 Conversation Memory
- 📂 Multi-Chat Management
- 🔊 Voice Responses
- 🏷️ Auto Chat Title Generation
- 🌍 Multilingual Support

No installation required — simply open the link and start chatting.
# 🗄️ Database Schema

## Chats Table

```sql
CREATE TABLE chats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
);
```

## Messages Table

```sql
CREATE TABLE messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    role TEXT,
    content TEXT
);
```

---

# 🔄 Application Workflow

```text
User
 │
 ▼
Voice / Text Input
 │
 ▼
Speech-to-Text (Whisper)
 │
 ▼
Conversation Context Builder
 │
 ▼
Groq LLM
 │
 ▼
AI Response
 │
 ├── Save to SQLite
 │
 └── Optional Text-to-Speech
          │
          ▼
      Audio Playback
```

---

# 🎯 Usage Example

### Voice Interaction

1. Click "🎤 Start Recording"
2. Speak your query
3. Click "⏹ Stop Recording"
4. Audio is transcribed
5. AI generates a response
6. Optional voice reply is played

---

### Text Interaction

**User**

```text
Explain blockchain in simple words.
```

**Assistant**

```text
Blockchain is a digital ledger that records transactions across many computers. It ensures data is secure, transparent, and cannot be easily modified.
```

---

# ✨ Sidebar Features

### Chat Management
- ➕ Create New Chat
- 💬 Select Existing Chat
- ✏️ Rename Chat
- 🗑 Delete Chat

### AI Configuration
- Select Model
- Enable/Disable Voice Reply

---

# 🔒 Security Notes

Never commit secrets to GitHub.

Add the following to `.gitignore`

```gitignore
.streamlit/secrets.toml
chat.db
__pycache__/
*.pyc
```

---

# 🔮 Future Improvements

- Real-time streaming responses
- Language auto-detection
- User authentication
- Export chats as PDF
- Document-based chat (RAG)
- Cloud database integration
- Voice cloning
- Speech-to-speech conversations
- Sentiment analysis
- Conversation summaries

---

# 🤝 Contributing

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Add feature"
```

4. Push changes

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻Reecha

**Arpan**

Built with ❤️ using Streamlit, Groq, Whisper, SQLite, and Google Text-to-Speech.
