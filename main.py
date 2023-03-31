from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

from balancelib.interactors.response_api_interactor import ResponseError
from balancelib.routes import user_routes, bank_routes, nubank_routes

from database.settings import create_tables

create_tables()

app = FastAPI(app_name="balance")


@app.exception_handler(ResponseError)
async def unicorn_exception_handler(request: Request, exc: ResponseError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.error(),
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "hellow world"
    }


@app.get("/router2")
async def root():
    return {
        "message": "hellow world2"
    }

app.include_router(user_routes.router)
app.include_router(bank_routes.router)
app.include_router(nubank_routes.router)

handler = Mangum(app)
