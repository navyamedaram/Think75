from app.app import app
from app.libs.authJWT import AuthJWT
from fastapi import FastAPI,Depends,HTTPException,UploadFile,File
from app.utills.helper import process_file
from app.Schemas.assesmentSchema import AssessmentSchema,assessmentIdSchema,updateAssessmentSchema,idSchema
from pymongo import MongoClient
from app.libs.mongoConnection import mongoDBClient,collection
from bson.objectid import ObjectId
# from io import BytesIO
# import pandas as pd
from datetime import datetime


@app.post("/createAssessment")
def create_assessment(assessment: AssessmentSchema,Authorize:AuthJWT=Depends()):
    try:
        currentUser=Authorize.get_jwt_subject
        Dict=assessment.dict()
        Dict['userId']=currentUser
        # assessment.id=currentUser
        collection = mongoDBClient["adminAssessmentModel"]
        
        # Check if assessment with the same name exists
        existing_assessment = collection.find_one({"name": assessment.name})
        if existing_assessment:
            return {
                "status_code": 400,
                "message": "Assessment already exists"
            }
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(assessment.WorkspaceId)})
        if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            } 

        # Insert assessment data
        assessment_data = assessment.dict()
        assessment_data["created_by"] = "user_id_here" 
        if assessment_data["sponserId"] == "":
            assessment_data["sponserId"] = None
        collection.insert_one(assessment_data)

        return {
            "status_code": 200,
            "message": "Assessment created successfully"
        }
    except Exception as e:
        return {
            "status_code": 400,
            "message": str(e)
        }
# @app.post("/getAssessment")
# async def get_assessment(id: assessmentIdSchema):
@app.post("/getAssessment")
def get_assessment(assessment_id: assessmentIdSchema,Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_jwt_subject
        Dict=assessment_id.dict()
        Dict['userId']=currentUser
        # assessment_id.id=currentUser
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(assessment_id.WorkspaceId)})
        if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            } 
        collection = mongoDBClient["adminAssessmentModel"]
        
        assessment = collection.find_one({"_id":ObjectId(assessment_id.id)})

        if not assessment:
            return {
                "status_code": 400,
                "message": "Assessment not found"
            }
        else:
           assessment['_id'] = str(assessment['_id'])
           return {
            "status_code": 200,
            "message":"found data",
            "res":assessment
            # "data": assessment
        }
    # except Exception as e:
    #     return {
    #         "status_code": 400,
    #         "message": str(e)
    #     }


@app.post("/updateAssessment")
async def updateAssessment(assessment: updateAssessmentSchema, Authoriza: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        currentUser = Authoriza.get_jwt_subject()
        Dict=assessment.dict()
        Dict['userId']=currentUser
        # assessment.id=currentUser
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(assessment.WorkspaceId)})
        if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            } 
        assessment_id = ObjectId(assessment.id)
        existing_assessment = collection.find_one({"_id": assessment_id})

        if not existing_assessment:
            return {"status_code": 400,
                    "message": "Assessment not found"}
        else:
            # Update the assessment
            collection.update_one({"_id": assessment_id}, {"$set": assessment.dict()})

        return {"status_code": 200,
                "message": "Assessment updated successfully"}

    except Exception as e:
        return {"status_code": 400,
                "message": str(e)}


@app.post("/deleteAssessment")
async def deleteAssessment(id: idSchema, Authorize: AuthJWT = Depends()):
    try:
        # Authoriza.jwt_required()
        currentUser = Authorize.get_jwt_subject()
        Dict=id.dict()
        Dict['userId']=currentUser
        # id.id=currentUser
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(id.WorkspaceId)})
        if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            } 

        assessment_id = ObjectId(id.id)
        collection.delete_one({"_id": assessment_id})

        # if not assessment:
        #     return {"status_code": 400,
        #             "message": "Assessment not found"}
        # else:
        #     if assessment.get("status") == "deleted":
        return {"status_code": 200,
                        "message": "Assessment  deleted"}

            # # Update the assessment's status and deleted_at
            # collection.update_one({"_id": assessment_id}, {"$set": {
            #     "status": "deleted",
            #     "deleted_at": datetime.now()
            # }})

            # return {
            #     "status_code": 200,
            #     "message": "Assessment deleted successfully"
            # }

    except Exception as e:
        return {
            "status_code": 400,
            "message": "Assessment not found",
            "error": str(e)
        }
@app.get("/listAllAssessment")
def get_created_assessments(Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_raw_jwt
        collection = mongoDBClient["adminAssessmentModel"]

        assessments = collection.find().sort('_id', -1)
        print(assessments)
        assessment_list = []
        for list in assessments:
            list["_id"]=str(list['_id'])
            assessment_list.append(list)
        print(assessment_list)
        return {
            "status_code": 200,
            "data": assessment_list
        }
    # except Exception as e:
    #     return {
    #         "status_code": 400,
    #         "message": "Error retrieving assessments",
    #         "error": str(e)
    #     }