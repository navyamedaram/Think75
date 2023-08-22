from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List


class SkillSchema(BaseModel):
    id: Optional[str]
    skill: str
    parent: Optional[str]
    logo: Optional[str]
    description: Optional[str]
    
    
class SkillUpdateSchema(BaseModel):
    id: str
    skill: str
    parent: Optional[str]
    logo: Optional[str]
    description: Optional[str]
    
class SkillIdSchema(BaseModel):
    id: str        