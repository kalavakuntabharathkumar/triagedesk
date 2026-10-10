from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException
from app.config import settings
from app.schemas import TicketIn
from app.triage import triage
from app.store import connect,close,save,list_items,metrics
@asynccontextmanager
async def lifespan(app:FastAPI):
 await connect()
 yield
 await close()
app=FastAPI(title=settings.app_name,version="1.0.0",description="Support ticket classification and response suggestions",lifespan=lifespan)
@app.get("/health")
async def health():return {"status":"ok","storage":"mongodb" if settings.mongodb_url else "in-memory demo","llm_enabled":settings.llm_enabled}
@app.post("/api/tickets/triage")
async def triage_one(payload:TicketIn):
 result=await triage(payload);await save(result);return result
@app.post("/api/tickets/batch")
async def batch(payload:list[TicketIn]):
 if len(payload)>500:raise HTTPException(status_code=413,detail="Maximum 500 tickets per batch")
 out=[]
 for ticket in payload:
  result=await triage(ticket);await save(result);out.append(result)
 return {"processed":len(out),"results":out}
@app.get("/api/tickets")
async def tickets(limit:int=100):
 if limit<1 or limit>1000:raise HTTPException(status_code=400,detail="limit must be between 1 and 1000")
 return await list_items(limit)
@app.get("/api/metrics")
async def get_metrics():return await metrics()
