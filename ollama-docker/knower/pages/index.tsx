

import React, { useState, FormEvent } from 'react';

// EXAMPLE USING OLLAMA API
// curl ollama:11434/api/generate -d '{
//   "model": "mistral",
//   "prompt": "Why is the sky blue?"
// }'

interface ChatMessage {
  question: string;
  answer: string;
}

const HomePage: React.FC = () => {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [message, setMessage] = useState<string>('');

  const sendMessage = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:11434/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message, model: 'mistral', stream: false }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Response:', data);
      setChatHistory([...chatHistory, { question: message, answer: data.response }]);
      setMessage('');
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <p>Q: {chat.question}</p>
            <p>A: {chat.answer}</p>
          </div>
        ))}
      </div>
      <div style={{ flex: 2, display: 'flex', flexDirection: 'column', padding: '20px' }}>
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {/* Chat messages display area (if needed) */}
        </div>
        <form onSubmit={sendMessage} style={{ display: 'flex', marginTop: 'auto' }}>
          <input
            type="text"
            value={message}
            style={{ flexGrow: 1 }}
            onChange={(e) => setMessage(e.target.value)}
          />
          <button type="submit">Senin</button>
        </form>
      </div>
    </div>
  );
};

export default HomePage;
