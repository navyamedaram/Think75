from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.Schemas.golbalSchemas import userStatusEnum
from enum import Enum
# class adminWorkspaceSchema(BaseModel):
#     id: Optional[str]
#     name: str
#     description: Optional[str]
#     color:Optional [str]
#     image: Optional[str]
#     status:Optional [userStatusEnum]=userStatusEnum.active
#     created_at: Optional[datetime] = datetime.now()
#     created_by: Optional[str]
#     updated_at: Optional[datetime]
#     deleted_at: Optional[datetime]
# class listworkspaceschema(BaseModel):
#     id: Optional[str]
#     name: str
#     description: Optional[str]
#     color:Optional [str]
#     image: Optional[str]
#     status:Optional [userStatusEnum]=userStatusEnum.active
#     created_at: Optional[datetime] = datetime.now()
#     created_by: Optional[str]
#     updated_at: Optional[datetime]
#     deleted_at: Optional[datetime]
# class updateworkspaceschema(BaseModel):
#     id:Optional[str]
#     name: str
#     description: Optional[str]
#     color:Optional [str]
#     image: Optional[str]
# class deleteworkspaceschema(BaseModel):
#     id:Optional[str]
# class AdminlistWorkspace(BaseModel):
#     id: str
#     created_by: str
class TenantcreateWorkspaceSchema(BaseModel):
    name: str
    id:str
    description: Optional[str]
    color:Optional [str]
    image: Optional[str]
    status:Optional [userStatusEnum]=userStatusEnum.active
    created_at: Optional[datetime] = datetime.now()
    created_by: Optional[str]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
class TenantupdateWorkspaceSchema(BaseModel):
    id:str
    name: str
    description: Optional[str]
    color: Optional[str]
    image: Optional[str]
    status: Optional[userStatusEnum]=userStatusEnum.active
    created_by: Optional[str]
    updated_at: Optional[datetime] = datetime.now()
class TenantWorkspaceIdSchema(BaseModel):
    id: str

class UserStatusEnum(str, Enum):
    active = "active"
    deleted = "deleted"