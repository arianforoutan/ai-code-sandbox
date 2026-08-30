# AI Agent Code Execution Sandbox 🛡️🤖

A secure, isolated, and autonomous AI Agent architecture that executes generated Python code safely inside Docker containers, supports CSV data analysis with Pandas, and features a self-correction loop.

---

## 🚀 Key Features

* **Secure Docker Sandbox:** Isolates code execution in a restricted container environment with strict resource limits (`mem_limit="512m"`, `network_mode="none"`) and automated timeout and resource cleanup to prevent leaks.
* **Autonomous Agent with Self-Correction:** Powered by LangChain and LLMs, the agent can write code, execute it, catch errors/empty results, fix its own code iteratively, and arrive at the correct output.
* **Advanced Data Analysis:** Capable of handling structured data (CSV files), parsing localized/Persian columns, performing data aggregations, and generating visual charts (Matplotlib/Seaborn).
* **FastAPI Backend:** Exposes clean RESTful endpoints supporting multipart file uploads (`multipart/form-data`) and text prompts.

---

## 📂 Project Structure

```text
├── main.py          # FastAPI application & API endpoints
├── agent.py         # LangChain agent runner & self-correction loop
├── sandbox.py       # Docker SDK container manager & security sandbox
├── Dockerfile       # Custom Python environment image definition
├── workspace/       # Dynamic workspace for uploaded files, scripts & charts (Git ignored)
└── requirements.txt # Python dependencies
