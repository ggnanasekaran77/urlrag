import uvicorn
from monitor_service import urls as msu
from monitor_service import status as mss
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
import urllib3


urllib3.disable_warnings()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Welcome to Monitoring Page"
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.get("/health", response_class=HTMLResponse)
async def health(request: Request):
    data = {
        "page": "Welcome to Monitoring Page"
    }
    return templates.TemplateResponse("health.html", {"request": request, "data": data})


@app.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    data = mss.http_status_code()
    return templates.TemplateResponse("status_url.html", {"request": request, "data": data})


@app.get("/refresh")
async def refresh():
    msu.csv_parse("sample.csv")
    return {"action": "refresh"}


@app.on_event("startup")
@repeat_every(seconds=600)
def periodic():
    msu.csv_parse("sample.csv")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
