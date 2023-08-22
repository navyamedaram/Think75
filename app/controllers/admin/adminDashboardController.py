from app.libs.mongoConnection import mongoDBClient,adminColl
from fastapi import FastAPI, Request, HTTPException, Depends,Response
from app.Schemas.adminAuthSchema import adminMeSchema,ChangePasswordSchema,adminUserUpdateSchema
from app.app import app
from app.libs.authJWT import AuthJWT
from app.confy.whitelist import admin_allowed_domain
import hashlib
from app.libs.redisClient import redisAdd
from datetime import datetime,timedelta
from app.libs.smsClient import sendsms
import random
from bson import ObjectId
from app.libs.msg91Email import sendmail
from app.tpls.smsTpls import sendOtpTpl 

@app.post("/me")
def me(Authorize: AuthJWT = Depends()):
    # try:
        userId = Authorize.get_jwt_subject()
        adminColl = mongoDBClient["adminCollection"]
        user = adminColl.find_one({"_id": ObjectId(userId)})
        if user == None:
            raise HTTPException(status_code=404, detail={
                "status_code": 404,
                "message": "User Not Found"
            })
        return HTTPException(status_code=200, detail={
            "status_code": 200,
            "message": "User Found",
            "user": adminMeSchema(**user)
        })
    # except Exception as e:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
@app.post("/changePassword")
def changePassword(user:ChangePasswordSchema, Authorize: AuthJWT = Depends()):
    # try:
        # userid = Authorize.get_jwt_subject()
        adminColl = mongoDBClient["adminCollection"]
        # user.oldPassword = sha256(user.oldPassword.encode()).hexdigest()
        userdata = adminColl.find_one(
            {"username": (user.username), "password": (user.oldPassword)})
        if userdata == None:
            raise HTTPException(status_code=404, detail={
                "status_code": 404,
                "message": "Invalid Credentials"
            })
        # user.newPassword = sha256(user.newPassword.encode()).hexdigest()
        res = adminColl.update_one({"username": (user.username)}, {
                                   "$set": {"password": user.newPassword}})
        if res.modified_count == 1:
            return HTTPException(status_code=200, detail={
                "status_code": 200,
                "message": "Password Changed Successfully"
            })
        else:
            raise HTTPException(status_code=500, detail={
                "status_code": 500,
                "message": "Something Went Wrong"
            })
    # except Exception as e:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
@app.post("/updateProfile")
def updateProfile(user: adminUserUpdateSchema, Authorize: AuthJWT = Depends()):

    # try:
        userId = Authorize.get_jwt_subject()
        Dict=user.dict()
        Dict['userId']=userId
        print(userId)
        if userId == None:
            return HTTPException(status_code=401, detail={
                 "status_code": 401,
                 "message": "Unauthorized"
                  })
        adminColl = mongoDBClient["adminCollection"]
        user.updatedAt = datetime.now()
        user.updatedBy = userId
        user = user.dict()
        user.pop("email")
        user.pop("status")
        user.pop("mobile")
        res = adminColl.update_one({"_id": ObjectId(userId)}, {

                                   "$set": user})
        if res.modified_count == 1:
            user = adminColl.find_one({"_id": ObjectId(userId)})
            return HTTPException(status_code=200, detail={
                 "status_code": 200,
                 "message": "Profile Updated Successfully",
                  "user": adminMeSchema(**user)
               })
        else:
            raise HTTPException(status_code=500, detail={

                "message":"Something Went Wrong",

                "status_code":500

                })
                    
@app.post("/logout")
def logout(Authorize: AuthJWT = Depends()):
    # try:
        access_token = {}
        
        return HTTPException(status_code=200, detail={
            "status_code": 200,
            "message": "Logout Successful"
        })
    # except Exception as e:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
