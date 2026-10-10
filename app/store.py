from datetime import datetime,timezone
from app.config import settings
memory=[]
client=None
collection=None
async def connect():
 global client,collection
 if settings.mongodb_url:
  try:
   from motor.motor_asyncio import AsyncIOMotorClient
   client=AsyncIOMotorClient(settings.mongodb_url,serverSelectionTimeoutMS=2500)
   await client.admin.command("ping")
   collection=client[settings.mongodb_database]["tickets"]
   await collection.create_index("ticket_id",unique=True)
  except Exception:
   if client:client.close()
   client=None;collection=None
async def close():
 global client
 if client:client.close();client=None
async def save(item):
 row={**item,"created_at":datetime.now(timezone.utc).isoformat()}
 if collection is not None: await collection.update_one({"ticket_id":item["ticket_id"]},{"$set":row},upsert=True)
 else:
  idx=next((i for i,v in enumerate(memory) if v["ticket_id"]==item["ticket_id"]),None)
  if idx is None:memory.append(row)
  else:memory[idx]=row
 return row
async def list_items(limit=100):
 if collection is not None:return await collection.find({},{"_id":0}).sort("created_at",-1).limit(limit).to_list(length=limit)
 return list(reversed(memory[-limit:]))
async def metrics():
 items=await list_items(10000);out={"total":len(items),"by_priority":{},"by_category":{}}
 for x in items:
  for key,field in [("by_priority","priority"),("by_category","category")]:out[key][x[field]]=out[key].get(x[field],0)+1
 return out
