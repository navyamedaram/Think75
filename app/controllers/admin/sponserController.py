from app.app import app
from app.Schemas.sponserSchema import sponserSchema,sponserIdSchema,sponserUpdateSchema
from app.libs.mongoConnection import sponser_collection,mongoDBClient
from fastapi import FastAPI,Depends,HTTPException
from app.libs.authJWT import AuthJWT
from bson import ObjectId

@app.post("/createSponser")
async def add_sponser(sponser: sponserSchema,Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_jwt_subject
        Dict=sponser.dict()
        # sponser.id=currentUser
        Dict['userId']=currentUser
        print(currentUser)
        # Check if the sponsor already exists
        existing_sponsor = sponser_collection.find_one({"name": sponser.name})
        if existing_sponsor:
            return {"status_code": 400, "message": "Sponsor already exists"}

        # Insert the new sponsor into the collection
        sponser_id = sponser_collection.insert_one(sponser.dict()).inserted_id

        return {"status_code": 200, "message": "Sponsor created successfully", "sponser_id": str(sponser_id)}

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail="Something went wrong")

@app.get("/listsponser")
def get_created_sponser(Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_raw_jwt
        sponser_collection = mongoDBClient["SponserCollection"]

        sponsers = sponser_collection.find().sort('_id', -1)
        print(sponsers)
        sponser_list = []
        for list in sponsers:
            list["_id"]=str(list['_id'])
            sponser_list.append(list)
        print(sponser_list)
        return {
            "status_code": 200,
            "data": sponser_list
        }

@app.post("/updateSponser")
async def update_sponser(sponser: sponserUpdateSchema,Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_jwt_subject
        Dict=sponser.dict()
        Dict['userId']=currentUser
        # Check if the sponsor exists by its ID
        existing_sponsor = sponser_collection.find_one({"_id": ObjectId(sponser.id)})

        if existing_sponsor is None:
            return {"status_code": 404, "message": "Sponsor not found"}

        # Check if the updated name conflicts with other sponsors
        if (
            sponser_collection.find_one(
                {"name": sponser.name, "_id": {"$ne": ObjectId(sponser.id)}}
            )
            is not None
        ):
            return {"status_code": 400, "message": "Sponsor already exists"}

        # Update the sponsor document
        sponser_collection.update_one(
            {"_id": ObjectId(sponser.id)},
            {"$set": sponser.dict(exclude={"id"})},
        )

        return {"status_code": 200, "message": "Sponsor updated successfully"}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Something went wrong")
@app.post("/deleteSponser")
async def delete_sponser(id: sponserIdSchema,Authorize:AuthJWT=Depends()):
    try:
        # Check if the sponsor exists by its ID
        existing_sponsor = sponser_collection.find_one({"_id": ObjectId(id.id)})

        if existing_sponsor is None:
            return {"status_code": 400, "message": "Sponsor not found"}

        # Delete the sponsor document
        sponser_collection.delete_one({"_id": ObjectId(id.id)})

        return {"status_code": 200, "message": "Sponsor deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong")