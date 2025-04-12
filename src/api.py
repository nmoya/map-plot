import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from rich.console import Console

from . import root
from .errors import HTTPError, NotFound
from .templates import templates

console = Console()
app = FastAPI()
app.include_router(root.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Seconds"] = str(process_time)
    return response


@app.middleware("http")
async def global_error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        console.print_exception(show_locals=False)
        if isinstance(e, HTTPError):
            return templates.TemplateResponse("4xx.html", {"request": request, "message": e.message})
        elif isinstance(e, NotFound):
            return templates.TemplateResponse("404.html", {"request": request, "message": e.message})
        else:
            return templates.TemplateResponse("5xx.html", {"request": request, "message": str(e)})
    return response
