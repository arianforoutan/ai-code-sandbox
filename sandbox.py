import docker
import os

class DockerSandbox:
    def __init__(self, workspace_dir: str = "./workspace"):
        self.client = docker.from_env()
        self.workspace_dir = os.path.abspath(workspace_dir)
        os.makedirs(self.workspace_dir, exist_ok=True)
        
        self.image_name = "ai-sandbox-python:latest"
        self._build_image_if_needed()

    def _build_image_if_needed(self):
        try:
            self.client.images.get(self.image_name)
        except docker.errors.ImageNotFound:
            print("Building custom Docker sandbox image (this may take a minute)...")
            dockerfile_path = os.path.dirname(os.path.abspath(__file__))
            self.client.images.build(
                path=dockerfile_path,
                tag=self.image_name,
                rm=True
            )
            print("Docker image built successfully!")

    def run_code(self, code: str) -> dict:
        script_path = os.path.join(self.workspace_dir, "script.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            container = self.client.containers.run(
                self.image_name,
                command="python /workspace/script.py",
                volumes={self.workspace_dir: {'bind': '/workspace', 'mode': 'rw'}},
                working_dir="/workspace",
                network_mode="none",  
                mem_limit="512m",     
                detach=True
            )
            
            result = container.wait(timeout=10)
            logs = container.logs(stdout=True, stderr=True).decode('utf-8')
            container.remove()
            
            return {
                "exit_code": result.get("StatusCode", -1),
                "output": logs,
                "error": "" if result.get("StatusCode", -1) == 0 else logs
            }
        except Exception as e:


            try:
                container.kill()
                container.remove(force=True)
            except:
                pass
            
            return {
                "exit_code": -1,
                "output": "",
                "error": str(e)
            }