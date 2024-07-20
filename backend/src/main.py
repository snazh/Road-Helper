import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.api.auth_router import router as auth_router
from backend.src.api.roadsigns_router import router as roadsigns_router
from backend.src.api.user_router import router as user_router

# creating main app
app = FastAPI(
    title="Road Helper"
)

# including all routers
app.include_router(roadsigns_router)
app.include_router(user_router)
app.include_router(auth_router)
# Configuring API endpoints for Front-End
origins = [
    "http://localhost:3000",
]
# Configuring Middleware and CORS for Front-End
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],  # Allowed Methods (do not use *)
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
