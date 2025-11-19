# Handle both relative and absolute imports for local development and deployment
try:
    # Try relative imports first (for local development)
    from . import database
    from .api import overview_router, project_list_router, project_statistics_router
except ImportError:
    # Fallback to absolute imports (for deployment)
    import database
    from api import overview_router, project_list_router, project_statistics_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with SQLite"}

# Registering the routers
app.include_router(overview_router)
app.include_router(project_list_router)
app.include_router(project_statistics_router)