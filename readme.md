Resume-Based Q&A System
This project implements a resume-based question-answering system using LlamaIndex, FastAPI, and Google's Gemini models. It allows users to query a resume via a POST endpoint (/query), retrieving answers strictly from the resume content. The system evolved from an OpenAI-based implementation to a Gemini-based one to address API quota issues and simplify memory usage.
Prerequisites

Python: Version 3.8 or higher.
Virtual Environment: Recommended for dependency management.
Google AI Studio API Key: Required for Gemini models (obtain from Google AI Studio).
Dependencies:
llama-index-core
llama-index-llms-google-genai
llama-index-embeddings-google-genai
fastapi
uvicorn
requests (for testing with response.py)



Setup Instructions
Step 1: Set Up the Virtual Environment
Create and activate a virtual environment to manage dependencies.
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Step 2: Install Dependencies
Install the required Python packages.
pip install --upgrade llama-index-core llama-index-llms-google-genai llama-index-embeddings-google-genai fastapi uvicorn requests

Verify installation:
pip list | grep -E "llama-index|fastapi|uvicorn|requests"

Expected output (versions may vary):
llama-index-core                  0.11.0
llama-index-llms-google-genai     0.2.0
llama-index-embeddings-google-genai 0.2.0
fastapi                           0.115.0
uvicorn                           0.30.1
requests                          2.32.3

Step 3: Configure Google API Key
Set your Google AI Studio API key as an environment variable.
export GOOGLE_API_KEY='your-gemini-api-key'  # Replace with your actual key
# On Windows: set GOOGLE_API_KEY=your-gemini-api-key

Test the key:
from llama_index.llms.google_genai import GoogleGenAI
llm = GoogleGenAI(model="models/gemini-1.5-flash")
print(llm.complete("Test").text)

If this fails, verify your key in Google AI Studio and ensure access to models/embedding-001 and gemini-1.5-flash.
Step 4: Initial Attempt with OpenAI (and Error)
The initial code (resume_qa_system.py) used OpenAI for embeddings and LLM but failed with:
openai.RateLimitError: Error code: 429 - {'error': {'message': 'You exceeded your current quota...'}}

This occurred because the OpenAI API key hit a quota limit. To resolve this, the system was modified to use Google’s Gemini models, which you confirmed having a valid API key for.
Step 5: Switch to Gemini and Address Memory Issues
The OpenAI-based code was updated to use Gemini for both embeddings and LLM (resume_qa_system_gemini_simple.py). An earlier version used Hugging Face embeddings (sentence-transformers/all-MiniLM-L6-v2), but it required significant memory, leading to the adoption of Gemini’s cloud-based embedding-001 model to minimize local resource usage.
Step 6: Fix Deprecation Warnings
The initial Gemini-based code used deprecated classes (GeminiEmbedding, Gemini), causing warnings:
/home/mathankumar/Downloads/resume_qa/resume_qa_system.py:62: DeprecationWarning: Call to deprecated class GeminiEmbedding...
/home/mathankumar/Downloads/resume_qa/resume_qa_system.py:63: DeprecationWarning: Call to deprecated class Gemini...

These were resolved by updating to GoogleGenAIEmbedding and GoogleGenAI from llama-index-embeddings-google-genai and llama-index-llms-google-genai.
Step 7: Address 404 Not Found Error
Accessing http://localhost:8000 in a browser returned {"detail":"Not Found"} because the application only defined a POST /query endpoint. A root endpoint (@app.get("/")) was added to provide a helpful message:
{
  "message": "Resume Q&A System. Use POST /query with a JSON query (e.g., {\"query\": \"Tell me about yourself\"})."
}

Step 8: Run the Application
Save the final code as resume_qa_system_gemini_simple.py (provided in the conversation history). Run the server:
python resume_qa_system_gemini_simple.py

Expected log:
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

Step 9: Test the /query Endpoint
Test the system by sending a POST request to http://localhost:8000/query.
Using curl
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"query": "Tell me about yourself"}'

Expected Output
{
  "query": "Tell me about yourself",
  "response": "I am a Machine Learning Engineer with 3+ years of experience specializing in building scalable AI solutions. My work includes projects on healthcare transcription, generative AI, LLM fine-tuning, and deployment using FastAPI and GCP."
}

Other Example Queries

Skills:curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"query": "What are your skills?"}'

Output:{
  "query": "What are your skills?",
  "response": "My skills include programming in Python, Java, and C++, using frameworks such as TensorFlow, PyTorch, and FastAPI, working with cloud platforms like Google Cloud Platform (GCP) and AWS, and expertise in AI/ML areas such as LLM fine-tuning, generative AI, and computer vision."
}


Unanswerable Query:curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"query": "What is your favorite hobby?"}'

Output:{
  "query": "What is your favorite hobby?",
  "response": "This information is not available in the resume"
}



Step 10: Test with a Python Script (response.py)
To test the endpoint programmatically, create a Python script named response.py.

```python
import requests

def query_resume(question):    url = "http://localhost:8000/query"    payload = {"query": question}    headers = {"Content-Type": "application/json"}    try:        response = requests.post(url, json=payload, headers=headers)        response.raise_for_status()  # Raise an error for bad status codes        return response.json()    except requests.exceptions.RequestException as e:        return {"error": f"Failed to query endpoint: {str(e)}"}
if name == "main":    # Example queries    queries = [        "Tell me about yourself",        "What are your skills?",        "What is your favorite hobby?"    ]    for query in queries:        result = query_resume(query)        print(f"Query: {query}")        print(f"Response: {result}")        print("-" * 50)```
