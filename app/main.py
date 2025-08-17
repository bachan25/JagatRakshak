from fastapi import FastAPI
from app.routes import incidents_controller, user_controller, location_controller, notify_controller,template_controller, vehicle_info_controller, tavily_mcp_controller
from fastapi.middleware.cors import CORSMiddleware

from app.models import users,incidents
from app.db.database import engine

# Create DB tables
users.Base.metadata.create_all(bind=engine)
incidents.Base.metadata.create_all(bind=engine)


app = FastAPI(
            title="JagatRakshak Emergency Response API",
            description="API for handling emergency reports and notifications",
            version="1.0.0",
            docs_url="/api/docs",
            redoc_url="/api/redoc",
            openapi_url="/api/openapi.json"
            )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","https://jagatrakshak.loca.lt"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(incidents_controller.router, prefix="/api/incidents", tags=["Incidents"])
app.include_router(notify_controller.router, prefix="/api/notify", tags=["Notifications"])
app.include_router(user_controller.router, prefix="/api/users", tags=["Users"])
app.include_router(location_controller.router, prefix="/api/location", tags=["Location"])
app.include_router(template_controller.router, prefix="/api/template", tags=["HTML Template"])
app.include_router(vehicle_info_controller.router, prefix="/api/vehicle", tags=["Vehicle Information"])
app.include_router(tavily_mcp_controller.router, prefix="/api/tavily", tags=["Tavily MCP"])

