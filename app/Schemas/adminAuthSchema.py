from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.utills.pyObjId import PyObjectId
from datetime import datetime
from enum import Enum
from datetime import datetime
from app.Schemas.golbalSchemas import userStatusEnum

class adminsgnupschema(BaseModel):
    username:Optional[str]
    userid:Optional[str]
    password:Optional[str]
    email:Optional[str]
    mobile:Optional[str]
    Dob:Optional[str]
    address:Optional[str]
    gender:Optional[str]
    jobRole:Optional[str]
    city:Optional[str]
    country:Optional[str]
    college:Optional[str]

class adminLoginSchema(BaseModel):
    email: EmailStr
    password: str 
class adminForgotPasswordSchema(BaseModel):
    email:EmailStr
class verifyOtpSchema(BaseModel):
    mobileOtp: str
    email:str
class adminPasswordSchema(BaseModel):
    email:str
    password: str
    otp:Optional[str]

class adminRoleEnum(str, Enum):
    "Admin Role Enum"
    admin = "admin"
    superAdmin = "superAdmin"
    moderator = "moderator"
    creator = "creator"

class adminMeSchema(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id")
    id:Optional[PyObjectId]
    name: Optional[str]
    email: EmailStr 
    mobile: str 
    role: Optional[adminRoleEnum] = adminRoleEnum.moderator
    profilePic: Optional[str]
    isMobileVerified: Optional[bool] = False
    isEmailVerified: Optional[bool] = False
    mfa: Optional[bool] = False
    status: Optional[userStatusEnum] = userStatusEnum.active
    createdBy: Optional[PyObjectId]
    createdAt: Optional[datetime] = datetime.now()
    updatedAt: Optional[datetime]
    updatedBy: Optional[PyObjectId]
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PyObjectId: str
        }
class ChangePasswordSchema(BaseModel):
    username:str
    oldPassword: str 
    newPassword: str
class adminUserUpdateSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    username: Optional[str]
    email: Optional[EmailStr]
    mobile: Optional[str]
    role: Optional[adminRoleEnum]
    profilePic: Optional[str]
    status: Optional[userStatusEnum]
    updatedAt: Optional[datetime] = datetime.now()
    updatedBy: Optional[PyObjectId]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            PyObjectId: str
        }
# class adminMeUpdateSchema(BaseModel):
#     id:str
#     username: Optional[str]
#     mobile: Optional[str]
#     profilePic: Optional[str]
#     updatedAt: Optional[datetime] = datetime.now()