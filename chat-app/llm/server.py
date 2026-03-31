from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Load model (replace with smollm2 if needed)
generator = pipeline("text-generation", model="HuggingFaceTB/SmolLM2-360M-Instruct")

class ChatRequest(BaseModel):
    model: str
    messages: list


@app.get("/v1/models")
def list_models():
    return {"data": [{"id": "smollm2"}]}


@app.post("/v1/chat/completions")
def chat(req: ChatRequest):
    user_message = req.messages[-1]["content"]

    result = generator(user_message, max_length=100, do_sample=True)

    return {
        "choices": [
            {
                "message": {
                    "content": result[0]["generated_text"]
                }
            }
        ]
    }
