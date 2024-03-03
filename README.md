# RAG_QA
A serverless RAG QA bot for various clients

[Architectural Diagram](https://whimsical.com/3HRNtxuciPMTLWmenb3b6q)

Setup:
1. Clone the repo
2. run `pip3 install -r requirements.txt`
2. Install ollama and make sure the server is running
3. Download the LLM with `ollama pull mistral`
4. Start the server with `uvicorn api:app --host 0.0.0.0 --port 1337 --reload`
5. Try it out with `curl -X POST http://localhost:1337/ask -H "Content-Type: application/json" -d '{"question": "What is the sky blue?"}'`


UI
`nvm install 18`
`nvm use`
`npm run dev`

Docker Setup:+

1. Install Docker
2. Install Docker Compose
3. Run Ollama
  - `cd ollama-docker`
  - `docker-compose up -d `
  - `docker-compose -f docker-compose-ollama-gpu.yaml up -d`  // if you have a nvidia GPU configured

  - https://locahost:8000 to see whats running
  - https://localhost:11434 ollama service
  - https://localhost:3000 to see the UI
to download the model 
  `docker ps` shows all docker instances running
   enter the ollama container with:  `docker exec -it ollama bash`
    `ollama pull mistral` ADD THIS TO THE DOCKER FILE
    `ollama run mistral` TO TEST ITS WORKING

TODO: 
  Pull Mistrall automatically at build of the container



