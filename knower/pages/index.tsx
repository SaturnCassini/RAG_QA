

import React, { useState, FormEvent } from 'react';


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
      const response = await fetch('http://localhost:1337/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: message }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
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
          <button type="submit">Send</button>
        </form>
      </div>
    </div>
  );
};

export default HomePage;
