from app.app import app
from app.Schemas.adminSkillSchema import SkillSchema,SkillIdSchema,SkillUpdateSchema
from bson import ObjectId
from app.libs.authJWT import AuthJWT
from fastapi import FastAPI,Depends,HTTPException
from app.libs.mongoConnection import skills_collection
from datetime import datetime
@app.post('/add_skill')
def addSkill(skill: SkillSchema, Authorize: AuthJWT = Depends()):
    try:
        currentUser = Authorize.get_raw_jwt()
        SkillSchema.id=currentUser

        skill_data = skills_collection.find_one({"skill": skill.skill})
        if skill_data:
            return {"status_code": 400, "message": "Skill already exists"}

        # Insert the skill document into MongoDB
        result = skills_collection.insert_one(skill.dict())

        return {"status_code": 200, "message": "Skill added successfully", "skill_id": str(result.inserted_id)}
        
    except Exception as e:
        return {"status_code": 400, "message": "Skill not added", "error": str(e)}
    

@app.post("/updateskill")
async def updateskill(skill:SkillUpdateSchema,Authorize: AuthJWT = Depends()):  
    currentUser=Authorize.get_jwt_subject()
    skillDict=skill.dict()
    skillDict['userId']=currentUser
    print(skillDict)
    result=skills_collection.update_one({"_id":ObjectId(skillDict['id'])},{"$set":skillDict})
    if result.modified_count>0:

            return{
                    "status_code":200,
                    "message":"skill updated successfully"
            }
    else:
             return{
                  "status_code":400,
                  "message":"not updated"
             }
    # return {"status_code":200,"message":"skill updated successfully"}

@app.post("/deleteskill")
async def deleteskill(id:SkillIdSchema, Authorize: AuthJWT=Depends()):
    currentUser=Authorize.get_jwt_subject()
    id_dict=id.dict()
    id_dict['userId']=currentUser
    skills_collection.delete_one({"_id":ObjectId(id.id)})
    return{
        "message":"skill deleted",
        "staus_code":200
    }

@app.get("/getallskills")
def get_created_skill(Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_raw_jwt
        # skills_collection = mongoDBClient["adminskillcollection"]

        Skills = skills_collection.find().sort('_id', -1)
        print(Skills)
        skill_list = []
        for list in Skills:
            list["_id"]=str(list['_id'])
            skill_list.append(list)
        print(skill_list)
        return {
            "status_code": 200,
            "data": skill_list
        }

