import logging as logger
import time
from monitor_service import urls as msu
from monitor_service import status as mss
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every


# logger = logging.getLogger(__name__)
app = FastAPI()
counter = 0


@app.get('/status')
async def root():
    return {"http_status_code": mss.http_status_code()}


@app.on_event("startup")
@repeat_every(seconds=5, logger=logger, wait_first=True)
def periodic():
    msu.csv_parse("sample.csv")