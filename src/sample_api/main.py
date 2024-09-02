from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .v1.routes.housing_type_routes import router as housing_type_router
from .v1.routes.housing_routes import router as housing_router
from .core.config import Configuration

api_prefix_v1 = Configuration.API_V1_STR

_NAME = "Sample API"
_DESC = "A sample api using FastAPI, SQLAlchemy and Postgres"

OpenAPIInfo = {
    "title": _NAME,
    "version": "0.1.0",
    "description": _DESC
}
tags_metadata = [
    {
        "name": _NAME,
        "description": _DESC,
    },
]

app = FastAPI(title=OpenAPIInfo["title"],
              version=OpenAPIInfo["version"],
              openapi_tags=tags_metadata, )

app.add_middleware(
    CORSMiddleware,
    allow_origins=Configuration.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Sample API"}


app.include_router(housing_type_router,
                   prefix=api_prefix_v1 + '/housing_type',
                   tags=["Housing Types"])


app.include_router(housing_router,
                   prefix=api_prefix_v1 + '/housing',
                   tags=["Housing"])
