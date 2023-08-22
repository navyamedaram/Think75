from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.Schemas.golbalSchemas import userStatusEnum,difficultyEnum
from enum import Enum
from fastapi import FastAPI
class adminassesmentSchema(BaseModel):
    workspace_id: str
    
class AssessmentSchema(BaseModel): 
    name : str
    id:Optional[str]
    color : Optional[str]
    description : Optional[str]
    instructions : Optional[str]
    WorkspaceId : Optional[str]
    duration :Optional[int]
    difficultyLevel:Optional[difficultyEnum]=difficultyEnum.medium
    totalMarks : Optional[int] 
    negativeMarks : Optional[float]
    passMarks : Optional[int]
    showResult : Optional[bool]
    status:Optional[userStatusEnum]=userStatusEnum.active
    bannerImage : Optional[str]
    sponserId : Optional[str]
    registered: Optional[int]
    qualified:Optional[int]
    completed:Optional[int]
    disableRightClick:Optional[bool]
    disableCopyPaste:Optional[bool]
    startWithFullScreen:Optional[bool]
    submitOnTabSwitch:Optional[bool]
    enableWebCam:Optional[bool]
    enableMicrophone:Optional[bool]
    allowMobile:Optional[bool]
    mfaVerification:Optional[bool]
    isEmailOtpVerified : Optional[bool]
    created_by : Optional[int]
    created_at :Optional[datetime] = datetime.now()
    updated_at :Optional[datetime] = datetime.now()
    deleted_at :Optional[datetime]

class assessmentIdSchema(BaseModel):
    id: Optional[str] 
    WorkspaceId: Optional[str]
    # status: Optional[userStatusEnum]=userStatusEnum.active
# class idSchema(BaseModel):
#     id: Optional[str]  
#     email: Optional[str] 
#     workspace
class updateAssessmentSchema(BaseModel):
    id: str
    name: str
    color: str
    description: str
    WorkspaceId: str
    description: Optional[str]
    duration: Optional[int]
    totalMarks: Optional[int]
    passMarks: Optional[int]
    negativeMarks: Optional[int]
    difficultyLevel: Optional[difficultyEnum]=difficultyEnum.medium
    status: str="active"
    sponserId: Optional[int]
    examStartDate: Optional[datetime] = datetime.now()
    created_at: Optional[str]  = datetime.now()
    updated_at: Optional[str] = datetime.now()
    deleted_at: Optional[str] = datetime.now()
    examEndDate:Optional[datetime] = datetime.now()    
    
    # ... other fields
class idSchema(BaseModel):
    id: str
    WorkspaceId:str 
# class listschema(BaseModel):
#     name:str