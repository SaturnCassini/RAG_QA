import React, { useState, useEffect } from 'react';

const GenerateText = () => {
  const [result, setResult] = useState('');
  const [prompt, setPrompt] = useState('');

  const generateText = async () => {
    const requestData = {
      model: 'mistral:latest',
      prompt: prompt
    };

    try {
      const response = await fetch('http://localhost:11434/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let resultText = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        resultText += chunk;
        setResult(resultText);
      }
    } catch (error) {
      console.error('Error generating text:', error);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (result) {
        console.log(result);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [result]);

  return (
    <div>
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt"
      />
      <button onClick={generateText}>Generate Text</button>
      <p>{result}</p>
    </div>
  );
};

export default GenerateText;