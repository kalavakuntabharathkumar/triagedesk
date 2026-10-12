import pytest
from app.schemas import TicketIn
from app.triage import baseline
from app.store import save,list_items,metrics
def make(id="T-1",subject="Payment invoice issue",description="I was charged twice and need a refund.",tier="standard"):
 return TicketIn(ticket_id=id,subject=subject,description=description,customer_tier=tier)
def test_billing_category():assert baseline(make())["category"]=="billing"
def test_security_incident_critical():assert baseline(make("T-2","Security incident","Possible data breach affecting all users"))["priority"]=="critical"
def test_premium_high_priority():assert baseline(make("T-3","Question","Need information about service","premium"))["priority"]=="high"
def test_account_reply_security():assert "never send" in baseline(make("T-4","Login failed","Cannot sign in"))["suggested_reply"]
@pytest.mark.asyncio
async def test_store_and_metrics():
 await save(baseline(make("T-store","Delivery order","Tracking has not updated")))
 assert any(x["ticket_id"]=="T-store" for x in await list_items())
 assert (await metrics())["total"]>=1
