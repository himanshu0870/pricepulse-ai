from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from app.database import Base, engine
from app.routes import products, dashboard, settings as settings_route
from app.services.scheduler import PricePulseScheduler

Base.metadata.create_all(bind=engine)
app = FastAPI(title="PricePulse AI")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(products.router)
app.include_router(dashboard.router)
app.include_router(settings_route.router)

scheduler = PricePulseScheduler()

@app.on_event("startup")
def startup():
    scheduler.start(30)

@app.on_event("shutdown")
def shutdown():
    scheduler.shutdown()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html")
