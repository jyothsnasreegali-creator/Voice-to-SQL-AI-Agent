# 🎙️ Voice-to-SQL Agent (Local AI)

An AI-native application that allows users to interact with a SQLite database using natural language and voice commands. 

## 📺 Demo
![Project Demo](./demo.gif)
*If the GIF doesn't load, [watch the video here](https://github.com/jyothsnasreegali-creator/Voice-to-SQL-AI-Agent/issues/1)*

## 🛠️ Tech Stack
- **Frontend:** React.js (Web Speech API for STT/TTS)
- **Backend:** Flask, SQLAlchemy
- **AI Engine:** Ollama (qwen2.5-coder:7b)
- **Database:** SQLite

## 🚀 How to Run Locally
1. **Model:** Install [Ollama](https://ollama.com) and run `ollama run qwen2.5-coder:7b`.
2. **Backend:** - `cd backend`
   - `pip install -r requirements.txt`
   - `python app.py`
3. **Frontend:**
   - `cd frontend`
   - `npm install`
   - `npm start`
