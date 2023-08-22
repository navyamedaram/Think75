from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class sectionListSchema(BaseModel):
    id:Optional[str]
    sectionDetails: dict
    assessmentId: str
    WorkspaceId: str
    createdAt: Optional[datetime] = datetime.now()
    
    
class updateSectionListSchema(BaseModel):
    sectionDetails: dict
    id: str 
    WorkspaceId:str
    assesmentId:str   
    
class idSchema(BaseModel):
    id: str 
    WorkspaceId:str
    assesmentId:str  
    
class idSchemas(BaseModel):
    assessmentId: str
    workspaceId: str
class deleteSchema(BaseModel):
    id:str 
    WorkspaceId:str
    assesmentId:str 
