from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any,Text
from datetime import datetime
from app.Schemas.golbalSchemas import userStatusEnum
import json


class planModel(BaseModel):
    moduleNames: str
    credits : str
    duration: str
    
        

class paymentPlansSchema(BaseModel):
    id: Optional[str]
    name: str
    description: str
    modules:Optional [List[planModel]] 
    price: str
    currency: str
    status: Optional[userStatusEnum] = userStatusEnum.active
    updateExisting: Optional[bool] = False
    createdBy: Optional[str]
    createdAt: Optional[datetime] = datetime.now()
    updatedBy: Optional[str]

class paymentPlansUpdateSchema(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    price: Optional[str]
    modules:Optional [List[planModel]]
    currency: Optional[str]
    status: Optional[userStatusEnum] = userStatusEnum.active
    updateExisting: bool = False
    updatedAt: Optional[datetime] = datetime.now()
    updatedBy: Optional[str]

class paymentStrSchema(BaseModel):
    id: str

class paymentIntSchema(BaseModel):
    id: str