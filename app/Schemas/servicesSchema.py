from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum



class userStatusEnum(str, Enum):
    "User Status Enum"
    active = "active"
    inactive = "inactive"
    blocked = "blocked"
    deleted = "deleted"

class servicesSchema(BaseModel):
    id: Optional[str]
    name: str
    description: str
    status: Optional[userStatusEnum]= userStatusEnum.active
    image: Optional[str]
    createdAt: Optional[datetime] = datetime.now()
    updatedAt: Optional[datetime]
    updatedBy: Optional[int]
    
    
    
class servicesUpdateSchema(BaseModel):
    id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    status: Optional[userStatusEnum]= userStatusEnum.active
    image: Optional[str]
    updatedAt: Optional[datetime] = datetime.now()
    updatedBy: Optional[int]    
    
    
class serviceIdSchema(BaseModel):
    id: str   