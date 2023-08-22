from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from fastapi import  UploadFile
from app.Schemas.golbalSchemas import userStatusEnum,difficultyEnum




class newQuestionSchema(BaseModel):
    id:str
    assessmentid: Optional[str]
    Workspaceid: Optional[str]
    sectionId:Optional[str]
    tenant_id: Optional[str]
    tenant_sortname: Optional[str]
    user_id: Optional[str]
    question: str
    description: Optional[str]
    difficultyLevel: Optional[difficultyEnum]=difficultyEnum.medium
    type: str
    testCases: Optional[Any]
    examples:Optional[Any]
    numberOfExamples:Optional[int]
    exampleA: Optional[str]
    exampleB: Optional[str]
    exampleC: Optional[str]
    exampleD: Optional[str]
    exampleE: Optional[str]
    programmingLanguage: Optional[str]
    parameters: Optional[str]
    startupCode: Optional[str]
    studentCode: Optional[str]
    noOfTestCasesPassed: Optional[int]
    numberOfOptions: str
    imgUrl: Optional[str]
    optionA: Optional[str]
    optionB: Optional[str]
    optionC: Optional[str]
    optionD: Optional[str]
    optionE: Optional[str]
    selectedOptions: Optional[List]=None   
    
    
    
class newQuestionUpdateSchemaUpdate(BaseModel):
    id: Optional[str]
    assessmentid: Optional[str]
    Workspaceid: Optional[str]
    sectionId:Optional[str]
    question: Optional[str]
    type: Optional[str]
    numberOfOptions: Optional[str]
    testCases: Optional[Any]
    examples:Optional[Any]
    numberOfExamples:Optional[int]
    exampleA: Optional[str]
    exampleB: Optional[str]
    exampleC: Optional[str]
    exampleD: Optional[str]
    exampleE: Optional[str]
    programmingLanguage: Optional[str]
    parameters: Optional[str]
    startupCode: Optional[str]
    studentCode: Optional[str]
    noOfTestCasesPassed: Optional[int]
    imgUrl: Optional[str]
    optionA: Optional[str]
    optionB: Optional[str]
    optionC: Optional[str]
    optionD: Optional[str]
    optionE: Optional[str]
    selectedOptions: Optional[List]=None
    testCases: Optional[Any]
    programmingLanguage: Optional[str]
    parameters: Optional[str]
    startupCode: Optional[str]
    updatedBy: Optional[str]
class idSchema(BaseModel):
    id: Optional[str]
    assessmentid: Optional[str]
    Workspaceid: Optional[str]
    sectionId:Optional[str]
class getallquestions(BaseModel):
    assessmentid: Optional[str]
    Workspaceid:Optional[str]
    sectionid:Optional[str]
    # destination_workspace_id: Optional[str]   
class deletequestion(BaseModel):
    id:str
    assessmentid: Optional[str]
    Workspaceid: Optional[str]
    sectionId:Optional[str]   
    
       