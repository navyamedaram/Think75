from app.app import app
from app.Schemas.sectionSchema import sectionListSchema,idSchema,updateSectionListSchema,idSchemas,deleteSchema
from fastapi import FastAPI,Depends
from app.libs.authJWT import AuthJWT
from app.libs.mongoConnection import sectionCollection
from bson.objectid import ObjectId
from app.libs.mongoConnection import mongoDBClient

@app.post("/createSection")
async def createsection(section:sectionListSchema,Authorize: AuthJWT = Depends()):
    try: 
        currentUser=Authorize.get_raw_jwt() 
        section.id=currentUser
        workspaces_collection= mongoDBClient["WorkspaceCollection"]
        workspace = workspaces_collection.find_one({"_id": ObjectId(section.WorkspaceId)})
        if not workspace:
                return {
                    "status_code": 400,
                    "message": "Workspace not found"
                }
        collection=mongoDBClient["adminAssessmentModel"]
        assesment = collection.find_one({"_id": ObjectId(section.assessmentId)}) 
        if not assesment:
            return{
                "status_code":400,
                "message":"assesment not found"
            } 
        # if claims['type']=='classified':
        existing_section = sectionCollection.find_one({"sectionDetails": section.sectionDetails})
        if existing_section:
                return {
                    "status_code": 400,
                    "message": "section already exists"
                }
        sectionDict=section.dict()
        sectionCollection.insert_one(sectionDict)
        return {"status_code": 200,
                    "message": "section added successfully"}
    except Exception as e:
         return {
              "status_code":"400",
              "error":str(e)

         }

@app.post("/getSection")
async def getSection(id:idSchema,Authorize: AuthJWT = Depends()): 
    currentUser=Authorize.get_jwt_subject()
    Dict=id.dict()
    Dict['userId']=currentUser
    # id.id=currentUser
    # if claims['type']=='classified':
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(id.WorkspaceId)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(id.assesmentId)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    Sections=sectionCollection.find_one({"_id":ObjectId(id.id)})
    print(Sections)
    if not Sections:
        return{
            "status_code":400,
            "message":"section not found"
        }
    else:
        Sections['_id']=str(Sections['_id'])
        return{
            "message":"found_assesment",
            "status_code":200,
            "res":Sections
        }
   

@app.post("/updateSection")
async def updateSections(section:updateSectionListSchema,Authorize: AuthJWT = Depends()):  
    currentUser=Authorize.get_jwt_subject()
    Dict=section.dict()
    Dict['userId']=currentUser
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(section.WorkspaceId)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(section.assesmentId)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    # if claims['type']=='classified':
    sectionDict=section.dict()
    sectionCollection.update_one({"_id":ObjectId(section.id)},{"$set":sectionDict})
    return {"status_code":200,"message":"section updated successfully"}

@app.post("/getSections")
async def getSections(Authorize: AuthJWT = Depends()): 
    currentUser=Authorize.get_raw_jwt()
    # id.id=currentUser
    # if claims['type']=='classified': 
        # Authorize.jwt_required()
    allSections=sectionCollection.find().sort('_id, -1')
    print(allSections)
    data=[]
    for i in allSections:
        i["_id"]=str(i['_id'])
        data.append(i)
    print(data)
    return {
        "status_code":200,
        "data":data
        }
@app.post("/deleteSection")
def deleteSection(id:idSchema,Authorize: AuthJWT = Depends()):  
    # Authorize.jwt_required()
    currentUser=Authorize.get_jwt_subject()
    Dict=id.dict()
    Dict['userId']=currentUser
    # id.id=currentUser
    # if claims['type']=='classified':
    workspaces_collection= mongoDBClient["WorkspaceCollection"]
    workspace = workspaces_collection.find_one({"_id": ObjectId(id.WorkspaceId)})
    if not workspace:
            return {
                "status_code": 400,
                "message": "Workspace not found"
            }
    collection=mongoDBClient["adminAssessmentModel"]
    assesment = collection.find_one({"_id": ObjectId(id.assesmentId)}) 
    if not assesment:
        return{
            "status_code":400,
            "message":"assesment not found"
        } 
    result = sectionCollection.delete_one({"_id": ObjectId(id.id)})
    return {
            'message':'section  deleted',
            'status_code':200
            }
   