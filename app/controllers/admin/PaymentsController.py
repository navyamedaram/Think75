from app.app import app
from bson import ObjectId
from fastapi import FastAPI,Depends,HTTPException
from app.libs.mongoConnection import mongoDBClient,payment_plans_collection
from app.Schemas.PaymentsSchema import paymentPlansSchema,paymentPlansUpdateSchema,paymentIntSchema,paymentStrSchema
from app.libs.authJWT import AuthJWT

@app.post("/createPaymentPlan")
async def create_payment_plan(plan: paymentPlansSchema,Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_jwt_subject
        Dict=plan.dict()
        Dict['userId']=currentUser
        existing_service = payment_plans_collection.find_one({"name": plan.name})

        if existing_service:
            return {"status_code": 400, "message": "payment already exists"}

        # Add the new service to the collection
        Dict = plan.dict()
        payment_plans_collection.insert_one(Dict)

        return {"status_code": 200, "message": "payment added successfully"}

    # except Exception as e:
    #     raise HTTPException(status_code=400, detail="Service not added", error=str(e))

@app.post("/get_payments")
async def get_payments(Authorize:AuthJWT=Depends()):
    # try:
        currentUser=Authorize.get_raw_jwt
        # Retrieve all services from the MongoDB collection
        payments = payment_plans_collection.find().sort('_id', -1)
        print(payments)
        payment_list = []
        for list in payments:
            list["_id"]=str(list['_id'])
            payment_list.append(list)
        print(payment_list)
        return {
            "status_code": 200,
            "data": payment_list
        }
@app.post("/updatePaymentPlan")
async def update_payment_plan(plan_schema: paymentPlansUpdateSchema,Authorize:AuthJWT=Depends()):
    try:
        currentUser=Authorize.get_jwt_subject
        Dict=plan_schema.dict()
        Dict['userId']=currentUser
        # Check authorization here if needed

        # Convert the plan ID to ObjectId
        plan_id = ObjectId(plan_schema.id)

        # Check if the plan exists
        existing_plan = payment_plans_collection.find_one({"_id": plan_id})

        if existing_plan is None:
            return {
                "status_code": 200,
                "message": "Plan not found"
            }

        # Update the plan with the new data
        update_data = plan_schema.dict(exclude={"id"})
        update_result = payment_plans_collection.update_one(
            {"_id": plan_id},
            {"$set": update_data}
        )

        if update_result.modified_count == 1:
            return {
                "status_code": 200,
                "message": "Plan updated successfully"
            }
        else:
            return {
                "status_code": 500,
                "message": "Failed to update the plan"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.post("/deletepayment")
async def delete_payments(id: paymentIntSchema,Authorize:AuthJWT=Depends()):
    try:
        # Check if the sponsor exists by its ID
        existing_payment = payment_plans_collection.find_one({"_id": ObjectId(id.id)})

        if existing_payment is None:
            return {"status_code": 400, "message": "payment not found"}

        # Delete the sponsor document
        payment_plans_collection.delete_one({"_id": ObjectId(id.id)})

        return {"status_code": 200, "message": "payment deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong")
    
@app.post("/getPaymentPlan")
async def get_payment_plan(plainId: paymentStrSchema,Authorize:AuthJWT=Depends()):
    try:
        currentUser=Authorize.get_jwt_subject
        Dict=plainId.dict()
        Dict['userId']=currentUser
        # Check authorization here if needed

        # Convert the plan ID to ObjectId
        plan_id = ObjectId(plainId.id)

        # Retrieve the payment plan from the MongoDB collection by its ID
        plan_detail = payment_plans_collection.find_one({"_id": plan_id})

        if plan_detail is None:
            return {
                "status_code": 200,
                "message": "Plan not found"
            }

        # Convert the ObjectId to a string for the response
        plan_detail["_id"] = str(plan_detail["_id"])

        return {
            "details": plan_detail,
            "status_code": 200,
            "message": "Plan fetched successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))