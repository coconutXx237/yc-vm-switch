import subprocess
from fastapi import Request

from app.main import YC_VM_ID


def get_vm_status():
    try:
        result = subprocess.run(
            ["yc", "compute", "instance", "get", YC_VM_ID],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return "Unknown (Error)"
        output_lines = result.stdout.splitlines()
        status_line = next((line for line in output_lines if line.startswith("status:")), None)
        if status_line:
            return status_line.split(":")[1].strip()
        return "Unknown"
    except Exception as e:
        return f"Error: {str(e)}"


def start_vm():
    try:
        subprocess.run(["yc", "compute", "instance", "start", YC_VM_ID], check=True)
        return "VM started successfully"
    except subprocess.CalledProcessError:
        return "Failed to start VM"


def stop_vm():
    try:
        subprocess.run(["yc", "compute", "instance", "stop", YC_VM_ID], check=True)
        return "VM stopped successfully"
    except subprocess.CalledProcessError:
        return "Failed to stop VM"


def flash(request: Request, message: str, category: str):
    messages = request.session.get("messages", [])
    messages.append({"message": message, "category": category})
    request.session["messages"] = messages
