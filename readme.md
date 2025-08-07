# Resume Q&A System using FastAPI, LlamaIndex, and Gemini (Google GenAI)

This is a simple Resume Question & Answer system that leverages **Google's Gemini LLM**, **LlamaIndex**, and **FastAPI** to answer questions strictly based on the content of a resume.

---

## 📌 How It Works

- Loads a sample resume
- Indexes it using `LlamaIndex`
- Runs a local FastAPI server to accept questions
- Uses Gemini (Google GenAI) to answer those questions
- You can interact via a POST request or by using the provided `response.py` script

---

## 🔑 Step 1: Get a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Log in with your Google account
3. Click **"Get API Key"**
4. Copy the key and add it to your environment variables:

```bash
export GOOGLE_API_KEY=your_api_key_here
