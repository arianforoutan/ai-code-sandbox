import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from sandbox import DockerSandbox
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage

load_dotenv()

sandbox = DockerSandbox()

llm = ChatOpenAI(
    model="gpt-5-nano",
    openai_api_key=os.environ.get("GAPGPT_API_KEY"),
    openai_api_base=os.environ.get("GAPGPT_BASE_URL"),
    temperature=0.2
)

@tool
def execute_python_code(code: str) -> str:
    """Executes python code inside a secure isolated Docker sandbox and returns the output or error."""
    result = sandbox.run_code(code)
    if result["exit_code"] == 0:
        return f"SUCCESS:\n{result['output']}"
    else:
        return f"ERROR:\n{result['error']}"

class CodeAgentRunner:
    def __init__(self):
        self.llm = llm
        self.sandbox = sandbox  
        self.tools = {"execute_python_code": execute_python_code}
        self.llm_with_tools = llm.bind_tools([execute_python_code])

    def run(self, user_prompt: str, max_turns: int = 5) -> str:
        messages = [
            ("system", "You are an expert data analysis coding assistant. First, write a python script to inspect the columns of the CSV file if needed (e.g., print df.columns), then use the 'execute_python_code' tool. If you get an ERROR or unexpected zero/empty results, analyze the error, fix your code, and run it again until you get the correct answer. Finally, output the clear text result."),
            ("human", user_prompt)
        ]
        
        for _ in range(max_turns):
            response = self.llm_with_tools.invoke(messages)
            messages.append(response)
            
            if not response.tool_calls:
                return response.content
            
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                if tool_name in self.tools:
                    tool_func = self.tools[tool_name]
                    try:
                        tool_output = tool_func.invoke(tool_args)
                    except AttributeError:
                        tool_output = tool_func(**tool_args)
                    
                    messages.append(ToolMessage(
                        content=str(tool_output),
                        tool_call_id=tool_call["id"]
                    ))
        
        return "Agent reached max turns without finishing."