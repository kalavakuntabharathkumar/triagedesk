from pydantic import BaseModel,Field
from typing import Literal
class TicketIn(BaseModel):
 ticket_id:str=Field(min_length=1,max_length=100)
 subject:str=Field(min_length=2,max_length=300)
 description:str=Field(min_length=5,max_length=10000)
 customer_tier:Literal["free","standard","premium"]="standard"
