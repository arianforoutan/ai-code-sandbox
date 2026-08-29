from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import CodeAgentRunner

app = FastAPI(title="AI Agent Code Execution Sandbox")

agent_runner = CodeAgentRunner()

class AgentRequest(BaseModel):
    prompt: str

@app.post("/run-agent", response_model=None)
def run_agent_endpoint(request: AgentRequest) -> dict:
    try:
        result = agent_runner.run(request.prompt)
        return {
            "status": "Success",
            "agent_response": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))