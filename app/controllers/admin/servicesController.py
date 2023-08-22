from app.app import app
from app.Schemas.servicesSchema import servicesSchema,serviceIdSchema,servicesUpdateSchema
from app.libs.authJWT import AuthJWT
from fastapi import FastAPI,Depends,HTTPException
from app.libs.mongoConnection import mongoDBClient,services_collection
from bson import ObjectId
@app.post("/add_service")
async def add_service(service:servicesSchema,Authorize:AuthJWT=Depends() ):
    try:
        currentUser=Authorize.get_jwt_subject
        Dict=service.dict()
        Dict['userId']=currentUser
        # Check if the service already exists
        existing_service = services_collection.find_one({"name": service.name})

        if existing_service:
            return {"status_code": 400, "message": "Service already exists"}

        # Add the new service to the collection
        service_data = service.dict()
        services_collection.insert_one(service_data)

        return {"status_code": 200, "message": "Service added successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Service not added", error=str(e))
@app.post("/get_services")
async def get_services(Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_raw_jwt
        # Retrieve all services from the MongoDB collection
        services = services_collection.find().sort('_id', -1)
        print(services)
        service_list = []
        for list in services:
            list["_id"]=str(list['_id'])
            service_list.append(list)
        print(service_list)
        return {
            "status_code": 200,
            "data": service_list
        }
@app.post("/updateservices")
async def update_services(service: servicesUpdateSchema,Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_jwt_subject
        Dict=service.dict()
        Dict['userId']=currentUser
        # Check if the sponsor exists by its ID
        existing_sponsor = services_collection.find_one({"_id": ObjectId(service.id)})

        if existing_sponsor is None:
            return {"status_code": 404, "message": "Sponsor not found"}

        # Check if the updated name conflicts with other sponsors
        if (
            services_collection.find_one(
                {"name": service.name, "_id": {"$ne": ObjectId(service.id)}}
            )
            is not None
        ):
            return {"status_code": 400, "message": "Sponsor already exists"}

        # Update the sponsor document
        services_collection.update_one(
            {"_id": ObjectId(service.id)},
            {"$set": service.dict(exclude={"id"})},
        )

        return {"status_code": 200, "message": "Sponsor updated successfully"}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Something went wrong")
@app.post("/deleteservices")
async def delete_services(id: serviceIdSchema,Authorize:AuthJWT=Depends()):
    try:
        # Check if the sponsor exists by its ID
        existing_sponsor = services_collection.find_one({"_id": ObjectId(id.id)})

        if existing_sponsor is None:
            return {"status_code": 400, "message": "Sponsor not found"}

        # Delete the sponsor document
        services_collection.delete_one({"_id": ObjectId(id.id)})

        return {"status_code": 200, "message": "Sponsor deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong")