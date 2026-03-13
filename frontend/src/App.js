import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [tableData, setTableData] = useState([]);

  // 1. Voice Output (Agent Speaks)
  const speak = (text) => {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-IN'; 
    utterance.pitch = 1.0;
    utterance.rate = 1.1;
    window.speechSynthesis.speak(utterance);
  };

  // 2. Initial Greeting
  useEffect(() => {
    const greeting = "Hello Jyothsna! Your Voice to SQL agent is ready. How can I help you today?";
    setResponse(greeting);
    // Note: Click anywhere on the page if you don't hear this immediately (Browser security)
    speak(greeting);
  }, []);

  // 3. Voice Input (You Speak)
  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser.");
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event) => {
      setQuestion(event.results[0][0].transcript);
      setIsListening(false);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.start();
  };

  // 4. Submit to Backend
  const handleSubmit = async () => {
    if (!question) return;
    setLoading(true);
    setTableData([]); // Clear old table
    try {
      const res = await axios.post('http://127.0.0.1:5000/ask', { text: question });
      
      setResponse(res.data.response);
      setTableData(res.data.data || []); 
      speak(res.data.response);
    } catch (err) {
      const errText = "Hey! I'm having trouble connecting to the backend.";
      setResponse(errText);
      speak(errText);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🎙️ Voice-to-SQL Agent</h1>
      
      <div className="card">
        <textarea 
          value={question} 
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask me to create a table or show data..."
        />
        <div className="actions">
          <button onClick={handleVoiceInput} className={`btn-mic ${isListening ? 'active' : ''}`}>
            {isListening ? "Listening..." : "🎤 Speak"}
          </button>
          <button onClick={handleSubmit} disabled={loading} className="btn-submit">
            {loading ? "Processing..." : "Submit"}
          </button>
        </div>
      </div>

      {response && (
        <div className="response-box">
          <strong>Agent:</strong> {response}
        </div>
      )}

      {tableData.length > 0 && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                {Object.keys(tableData[0]).map((key) => <th key={key}>{key.toUpperCase()}</th>)}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((val, j) => <td key={j}>{String(val)}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;