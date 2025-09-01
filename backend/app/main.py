from fastapi import FastAPI

app = FastAPI(
    title="A Fervenza Tinta API",
    version="0.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs"
)
