import uvicorn
from fastapi import FastAPI, Request, HTTPException
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

print(os.getenv("LANGCHAIN_API_KEY"))
print(os.getenv("GROQ_API_KEY"))

## APIs

@app.post("/blogs")
async def create_blogs(request: Request):
    try:
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="Request body is empty")
        
        try:
            data = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")

        topic = data.get("topic", "")
        language = data.get("language", "")
        print(f"Received topic: {topic}, language: {language}")

        if not topic:
            raise HTTPException(status_code=400, detail="Topic is required")

        groqllm = GroqLLM()
        llm = groqllm.get_llm()

        graph_builder = GraphBuilder(llm)
        initial_state = {
            "topic": topic,
            "current_language": language.lower() if language else "",
            "blog": {"title": "", "content": ""}
        }

        if topic and language:
            graph = graph_builder.setup_graph(usecase="language")
            state = graph.invoke(initial_state)
        elif topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke(initial_state)
        else:
            raise HTTPException(status_code=400, detail="Topic is required")

        return {"data": {
            "topic": state["topic"],
            "current_language": state["current_language"],
            "blog": {
                "title": state["blog"]["title"],
                "content": state["blog"]["content"]
            }
        }}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)