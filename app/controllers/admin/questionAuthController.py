from app.app import app
from app.Schemas.questionSchema import newQuestionSchema,idSchema,newQuestionUpdateSchemaUpdate,getallquestions,deletequestion
from fastapi import FastAPI,Depends
from app.libs.authJWT import AuthJWT
from sqlalchemy.orm import Session
from app.libs.psqlDBClient import get_db
from app.libs.mongoConnection import mongoDBClient
from sqlalchemy import text
from app.libs.mongoConnection import newQuestion_admin_collection
from app.utills.helper import serializeList,serializeDict
from bson.objectid import ObjectId


@app.post('/createquestion')
async def create_question(question: newQuestionSchema, Authorize: AuthJWT = Depends()):
    # Authoriza.jwt_required()
    currentUser = Authorize.get_jwt_subject()
    question.id=currentUser
    Dict=question.dict()
    # Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(question.Workspaceid)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(question.assessmentid)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    sectionCollection=mongoDBClient["SectionCollection"]
    section=sectionCollection.find_one({"_id":ObjectId(question.sectionId)})
    if not section:
        return{
            "status_code":400,
            "message":"section not found"
        }
    existing=newQuestion_admin_collection.find_one({"question": question.question})
    if existing:
            return {"status_code": 400, "message": "question already exists"}

    newQuestion_admin_collection.insert_one(Dict)  
    return {"status_code":200,"message":"question added"}

@app.post('/getquestion')
async def get_question(getquestion:idSchema, Authorize: AuthJWT=Depends()):
    currentUser = Authorize.get_jwt_subject()
    Dict=getquestion.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(getquestion.Workspaceid)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(getquestion.assessmentid)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    sectionCollection=mongoDBClient["SectionCollection"]
    section=sectionCollection.find_one({"_id":ObjectId(getquestion.sectionId)})
    if not section:
        return{
            "status_code":400,
            "message":"section not found"
        }
    # getquestion.id=getId
    question=newQuestion_admin_collection.find_one({"_id":ObjectId(getquestion.id)})
    print(question)
    if not question:
        return{
            "status_code":400,
            "message":"question not found"
        }
    else:
        question['_id']=str(question['_id'])
        return{
            "message":"found_assesment",
            "status_code":200,
            "res":question
        }
@app.post("/updatequestion")
async def updatequestions(question:newQuestionUpdateSchemaUpdate,Authorize: AuthJWT = Depends()):  
    currentUser=Authorize.get_raw_jwt()
    Dict=question.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(question.Workspaceid)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(question.assessmentid)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    sectionCollection=mongoDBClient["SectionCollection"]
    section=sectionCollection.find_one({"_id":ObjectId(question.sectionId)})
    if not section:
        return{
            "status_code":400,
            "message":"section not found"
        }
    # if claims['type']=='classified':
    # questionDict=question.dict()
    newQuestion_admin_collection.update_one({"_id":ObjectId(Dict['id'])},{"$set":Dict})
    return {"status_code":200,"message":"question updated successfully"}

@app.post("/getallquestions")
async def getquestions(Authorize: AuthJWT = Depends()): 
    currentUser=Authorize.get_raw_jwt()
    # if claims['type']=='classified': 
        # Authorize.jwt_required()
    allquestions=newQuestion_admin_collection.find().sort('_id, -1')
    # print(allquestions)
    questions=[]
    for i in allquestions:
        i["_id"]=str(i['_id'])
        questions.append(i)
    print(questions)
    return {
        "status_code":200,
        "data":questions
        }
@app.post("/deletequestion")
async def delete_question(id:deletequestion, Authorize: AuthJWT=Depends()):
    currentUser=Authorize.get_raw_jwt()
    Dict=id.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(id.Workspaceid)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(id.assessmentid)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    sectionCollection=mongoDBClient["SectionCollection"]
    section=sectionCollection.find_one({"_id":ObjectId(id.sectionId)})
    if not section:
        return{
            "status_code":400,
            "message":"section not found"
        }
    delete=newQuestion_admin_collection.delete_one({"_id":ObjectId(id.id)})
    return{
        "message":"question deleted",
        "staus_code":200
    }


