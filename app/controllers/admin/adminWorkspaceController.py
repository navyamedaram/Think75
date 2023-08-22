from fastapi import Depends,HTTPException
from fastapi_jwt_auth import AuthJWT
from pymongo import MongoClient
from app.Schemas.workSpaceSchema import TenantcreateWorkspaceSchema,UserStatusEnum,TenantupdateWorkspaceSchema,TenantWorkspaceIdSchema
from app.Schemas.golbalSchemas import userStatusEnum
from bson import ObjectId
from fastapi import APIRouter
from app.app import app
from datetime import datetime,timedelta
from app.libs.mongoConnection import mongoDBClient,workspaces_collection

@app.get("/listWorkspace")
def get_created_workspaces(Authorize:AuthJWT=Depends()):
        
    # try:
        currentUser=Authorize.get_jwt_subject()
        # tenant_ws.id=currentUser
        workspaces_collection = mongoDBClient["WorkspaceCollection"]

        list_w = workspaces_collection.find().sort('_id', -1)
        print(list_w)
        workspace_list = []
        for list in list_w:
            list["_id"]=str(list['_id'])
            workspace_list.append(list)
        print(workspace_list)
        return {
            "status_code": 200,
            "data": workspace_list
        }

    
@app.post("/createWorkspace")
def create_workspace(tenant_ws: TenantcreateWorkspaceSchema,Authorize:AuthJWT=Depends()):

    try:
        # Check if the workspace already exists
        currentUser=Authorize.get_jwt_subject()
        tenant_ws.id=currentUser
        print(currentUser)
        existing_workspace = workspaces_collection.find_one({"name": tenant_ws.name})
        if existing_workspace:
            return {"status_code": 400, "message": "Workspace already exists"}

        # Add the created_by field
        getId = "your_user_id"  # Get the user ID from Authoriza (not shown in the code)
        tenant_ws_dict = tenant_ws.dict()
        tenant_ws_dict["created_by"] = getId

        # Insert the workspace data
        workspaces_collection.insert_one(tenant_ws_dict)

        
        return {"status_code": 200, "message": "Workspace created successfully"}
    except Exception as e:
        return {"status_code": 400, "message": "Something went wrong"}

@app.post("/updateWorkspace")
def update_workspace(tenant_update: TenantupdateWorkspaceSchema,Authorize: AuthJWT = Depends()):
    try:
   
        currentUser = Authorize.get_jwt_subject()
        workspaceDict=tenant_update.dict()
        workspaceDict['userId']=currentUser
        print(currentUser)
        # tenant_update.id=currentUser
        workspaces_collection=mongoDBClient["WorkspaceCollection"]
        adminBlogs = tenant_update.dict()
        adminBlogs["updatedAt"] = datetime.now()
        adminBlogs = {k: v for k, v in adminBlogs.items() if v is not None}
        result = workspaces_collection.update_one({"_id":ObjectId(tenant_update.id)}, {"$set": adminBlogs})

        return{
                "status_code":200,
                "message":"Workspace updated successfully"
                }
    except Exception as e:
        return HTTPException(status_code=400, detail={

              "status_code": 400,

              "message": "Something went wrong"

                })
@app.post("/deleteWorkspace")
def delete_workspace(tenant_delete: TenantWorkspaceIdSchema,Authorize:AuthJWT=Depends()):
    try:
        currentUser = Authorize.get_jwt_subject()
        Dict=tenant_delete.dict()
        Dict['userId']=currentUser
        # tenant_delete.id=currentUser
        # Check if the workspace exists
        query={"_id": ObjectId(tenant_delete.id)}
        print(query)
        existing_workspace = workspaces_collection.find_one(query)
        if existing_workspace is None:
            return {"status_code": 404, "message": "Workspace not found"}

        # Update the workspace to mark it as deleted
        workspaces_collection.delete_one(query)

        return {
            "status_code": 200,
            "message": "Workspace deleted successfully"
        }
    except Exception as e:
        return {"status_code": 400, "message": str(e)}


