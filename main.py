import platform
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from quarter_lib.logging import setup_logging

from api.router import api_router
from core.network_helper import log_request_info

logger = setup_logging(__file__)
app = FastAPI(debug=True)
app.include_router(api_router, dependencies=[Depends(log_request_info)])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.info(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get('/', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    '''
    Simple route for the GitHub Actions to healthcheck on.
    More info is available at:
    https://github.com/akhileshns/heroku-deploy#health-check
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in
    case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
      'healtcheck': 'Everything OK!'
    }
    '''
    return {'healthcheck': 'Everything OK!'}

if __name__ == "__main__":
    if platform.system() == "Windows":
        uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", reload=True, port=8100)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8100)
