import uvicorn
import urllib3

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every

from urlrag import urlchk, status as urlsrag_status

urllib3.disable_warnings()


log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(name)-15s - %(levelname)-6s - %(message)s"
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(name)-15s - %(levelname)-6s - %(message)s"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Welcome to URL RAG DashBoard"
    }

    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.get("/health", response_class=HTMLResponse)
async def health(request: Request):
    data = {
        "page": "Welcome to RAG DashBoard"
    }
    return templates.TemplateResponse("health.html", {"request": request, "data": data})


@app.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    data = urlsrag_status.main()
    return templates.TemplateResponse("status_url.html", {"request": request, "data": data})


@app.get("/refresh")
async def refresh():
    return {"action": "refresh"}


@app.on_event("startup")
@repeat_every(seconds=600)
def periodic():
    urlchk.main()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
