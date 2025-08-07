from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import os

# Initialize FastAPI app
app = FastAPI()

# Define input model for the query
class QueryRequest(BaseModel):
    query: str

# Sample resume content (stored in a file for LlamaIndex to process)
RESUME_CONTENT = """
# Sample Resume

## Personal Information
Name: Alex Doe
Profession: Machine Learning Engineer
Email: alex.doe@example.com

## Summary
I am a Machine Learning Engineer with 3+ years of experience specializing in building scalable AI solutions. My work includes projects on healthcare transcription, generative AI, LLM fine-tuning, and deployment using FastAPI and GCP.

## Experience
### Senior Machine Learning Engineer, AI Solutions Inc. (2022-Present)
- Developed and deployed healthcare transcription models using LLMs.
- Led a team to fine-tune generative AI models for content creation.
- Implemented scalable APIs using FastAPI and deployed on Google Cloud Platform (GCP).

### Machine Learning Engineer, TechCorp (2020-2022)
- Built computer vision models for object detection with 95% accuracy.
- Optimized model inference pipelines, reducing latency by 30%.
- Collaborated with cross-functional teams to integrate AI solutions into production.

## Education
- M.S. in Computer Science, University of Tech (2018-2020)
- B.S. in Computer Engineering, State University (2014-2018)

## Skills
- Programming: Python, Java, C++
- Frameworks: TensorFlow, PyTorch, FastAPI
- Cloud: Google Cloud Platform (GCP), AWS
- AI/ML: LLM fine-tuning, generative AI, computer vision
"""

# Save resume to a temporary file for LlamaIndex processing
def save_resume_to_file():
    os.makedirs("data", exist_ok=True)
    with open("data/resume.md", "w") as f:
        f.write(RESUME_CONTENT)

# Load and index resume using LlamaIndex
def initialize_index():
    save_resume_to_file()
    documents = SimpleDirectoryReader("data").load_data()
    
    # Configure Gemini for embeddings and LLM (assumes GOOGLE_API_KEY is set)
    Settings.embed_model = GoogleGenAIEmbedding(model_name="models/embedding-001")
    Settings.llm = GoogleGenAI(model="models/gemini-1.5-flash", temperature=0.2)
    
    # Create vector index
    index = VectorStoreIndex.from_documents(documents)
    return index

# Initialize index on startup
index = initialize_index()

# Define prompt template
PROMPT_TEMPLATE = """
You are a helpful assistant answering questions based strictly on the provided resume content. Do not generate any information not present in the resume. If the question cannot be answered with the resume content, respond with "This information is not available in the resume."

Resume content:
{context}

Question: {query}

Answer:
"""

@app.get("/")
async def root():
    return {"message": "Resume Q&A System. Use POST /query with a JSON query (e.g., {\"query\": \"Tell me about yourself\"})."}

@app.post("/query")
async def query_resume(request: QueryRequest):
    try:
        # Retrieve relevant content from the index
        query_engine = index.as_query_engine(similarity_top_k=3)
        
        # Construct prompt with retrieved context
        retriever = index.as_retriever()
        nodes = retriever.retrieve(request.query)
        context = "\n".join([node.text for node in nodes])
        
        prompt = PROMPT_TEMPLATE.format(context=context, query=request.query)
        
        # Query LLM with the prompt
        response = Settings.llm.complete(prompt).text
        
        return {
            "query": request.query,
            "response": response.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
