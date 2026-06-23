# 🎤 Multilingual Voice AI Copilot

A voice-enabled AI assistant built with Streamlit, Whisper, Ollama, SQLite, and gTTS.

This application allows users to interact with AI using either voice or text, maintain multiple chat sessions, and receive spoken responses in multiple languages.

---

## 🚀 Features

### 🎙️ Voice Input
- Record audio directly from the application
- Speech-to-text transcription using OpenAI Whisper
- Automatic language detection

### 🤖 AI Conversation
- Supports multiple Ollama models:
  - Llama 3
  - Mistral
  - Phi-3
- Context-aware conversations using chat history
- Maintains conversational memory within each chat session

### 🔊 Text-to-Speech
- Converts AI responses into speech
- Multilingual voice output using gTTS

### 💬 Chat Management
- Create new chats
- Rename existing chats
- Delete chats
- Persistent storage using SQLite

### 🌍 Multilingual Support
- Voice interaction in multiple languages
- Automatic language detection and response generation

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|------------|
| Frontend | Streamlit |
| Speech-to-Text | OpenAI Whisper |
| LLM Backend | Ollama |
| Database | SQLite |
| Text-to-Speech | gTTS |
| Audio Recording | SoundDevice |
| Audio Processing | SciPy |

---

## 📂 Project Structure

```text
voice-copilot/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── screenshots/
│   ├── home.png
│   ├── sidebar.png
│   └── voice-input.png
│
└── tests/
    └── test_ollama.py
```

---

## ⚙️ Prerequisites

Before running the project, install:

- Python 3.10+
- Ollama
- FFmpeg

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/multilingual-voice-ai-copilot.git

cd multilingual-voice-ai-copilot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🤖 Setup Ollama

Start Ollama:

```bash
ollama serve
```

Pull a model:

```bash
ollama pull llama3
```

You may also use:

```bash
ollama pull mistral
ollama pull phi3
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser automatically.

---

## 📸 Screenshots

### Main Interface

_Add screenshot here_

### Voice Input

_Add screenshot here_

### Chat Management

_Add screenshot here_

---

## 🔮 Future Improvements

- Browser-based microphone recording
- Cloud deployment
- User authentication
- Chat export functionality
- Semantic memory search
- Integration with online LLM APIs (OpenAI, Gemini, Groq)

---

## 🧠 Learning Outcomes

This project demonstrates:

- Speech Recognition
- Generative AI Integration
- Prompt Engineering
- Database Management
- Streamlit Application Development
- Multilingual AI Systems
- Voice User Interfaces

---

## 👨‍💻 Reecha

Built as a personal AI and speech technology project using modern open-source tools.

If you found this project useful, feel free to star ⭐ the repository.
