import docker
import tempfile
import os

class DockerSandbox:
    def __init__(self, image_name="python:3.10-slim"):
        # اتصال به داکر دسکتاپ روی سیستم میزبان
        self.client = docker.from_env()
        self.image_name = image_name

    def run_code(self, code_string: str, timeout: int = 10) -> dict:
        # ایجاد یک فایل موقت پایتون روی سیستم برای فرستادن کد به داخل کانتینر
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_string)
            temp_file_path = f.name

        container = None
        try:
            # ساخت و راه‌اندازی کانتینر داکر با تنظیمات امنیتی (ایزوله کامل)
            container = self.client.containers.create(
                self.image_name,
                command=f"python -c {repr(code_string)}",
                network_mode="none",  # قطع کامل دسترسی به اینترنت برای امنیت
                mem_limit="128m"      # محدودیت مصرف رم به 128 مگابایت
            )
            container.start()
            
            # انتظار برای پایان اجرای کد (با تعیین حد نصاب زمان یا Timeout)
            result = container.wait(timeout=timeout)
            logs = container.logs(stdout=True, stderr=True).decode('utf-8')
            
            exit_code = result.get("StatusCode", -1)
            return {
                "exit_code": exit_code,
                "output": logs,
                "error": None if exit_code == 0 else logs
            }
        except Exception as e:
            return {
                "exit_code": -1, 
                "output": "", 
                "error": f"Execution failed or timed out: {str(e)}"
            }
        finally:
            # پاکسازی و حذف کانتینر بعد از اتمام کار (جلوگیری از انباشته شدن کانتینرها در داکر دسکتاپ)
            if container:
                try:
                    container.remove(force=True)
                except:
                    pass
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)