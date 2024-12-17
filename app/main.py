from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse

from app.services import get_vm_status, start_vm, stop_vm


YC_VM_ID = "YC_VM_ID"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="admin")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    status = get_vm_status()
    messages = request.session.get("messages", [])
    request.session["messages"] = []
    return templates.TemplateResponse("index.html", {"request": request, "status": status, "messages": messages})


@app.post("/start")
async def start(request: Request):
    result = start_vm()
    request.session.setdefault("messages", []).append({"category": "success", "message": result})
    return RedirectResponse(url="/", status_code=303)


@app.post("/stop")
async def stop(request: Request):
    result = stop_vm()
    request.session.setdefault("messages", []).append({"category": "danger", "message": result})
    return RedirectResponse(url="/", status_code=303)
