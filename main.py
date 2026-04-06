import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage 
from src.graph import create_member360_graph
from src.models import CustomChatModel

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Member 360 API",
    description="Multi-Agent Backend for Healthcare Member 360 System"
)

# Initialize the Model and Graph once at startup
print("Initializing Healthcare Member 360 Multi-Agent System...")
llm = CustomChatModel()
graph_app = create_member360_graph(llm)

# Define request schema
class ChatRequest(BaseModel):
    member_id: str
    query: str

@app.post("/api/v1/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Process a user query, routing it through the appropriate agents
    and returning the steps and final output.
    """
    try:
        state = {
            "messages": [HumanMessage(content=request.query)],
            "next": "Supervisor",
            "member_context": {"member_id": request.member_id}
        }
        
        responses = []
        
        # Run graph execution
        for output in graph_app.stream(state):
            for node_name, result in output.items():
                step_data = {"node": node_name, "state_update": {}} 
                
                # Extract relevant context from the node's result
                if "messages" in result:
                    latest_message = result["messages"][-1].content
                    step_data["message"] = latest_message
                    # We avoid dumping the raw objects to avoid JSON serialization errors in FastAPI
                if "next" in result:
                    step_data["routing_to"] = result["next"]
                    step_data["state_update"]["next"] = result["next"]
                
                if "member_context" in result:
                    step_data["state_update"]["member_context"] = result["member_context"]
                    
                responses.append(step_data)
                
        return {
            "member_id": request.member_id,
            "query": request.query,
            "agent_steps": responses
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)