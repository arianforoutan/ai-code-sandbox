from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from agent import CodeAgentRunner
import os

app = FastAPI(title="AI Agent Code Execution Sandbox")

agent_runner = CodeAgentRunner()

@app.post("/run-agent", response_model=None)
async def run_agent_endpoint(
    prompt: str = Form(...),
    file: UploadFile = File(None)
) -> dict:
    try:
        file_info = ""
        if file:
            file_path = os.path.join(agent_runner.sandbox.workspace_dir, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            file_info = f"\n[System Note: The user uploaded a file named '{file.filename}'. You can load it using pandas: pd.read_csv('{file.filename}')]"

        full_prompt = prompt + file_info

        result = agent_runner.run(full_prompt)
        report_path = os.path.join(agent_runner.sandbox.workspace_dir, "analysis_report.md")
        with open(report_path, "a", encoding="utf-8") as md_file:
            md_file.write(f"# تحلیل جدید\n\n**سوال کاربر:** {prompt}\n\n{result}\n\n---\n\n")
        return {
            "status": "Success",
            "agent_response": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))