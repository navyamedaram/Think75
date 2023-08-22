from app.Schemas.adminAuthSchema import adminLoginSchema,adminsgnupschema,adminForgotPasswordSchema,verifyOtpSchema,adminPasswordSchema
from app.libs.mongoConnection import mongoDBClient,adminColl
from fastapi import FastAPI, Request, HTTPException, Depends,Response
from app.app import app
from app.libs.authJWT import AuthJWT
from app.confy.whitelist import admin_allowed_domain
import hashlib
from datetime import datetime,timedelta
from app.libs.smsClient import sendsms
import random
from bson import ObjectId
from app.libs.msg91Email import sendmail
from app.tpls.smsTpls import sendOtpTpl 

@app.post("/signup")
async def singup(seeker:adminsgnupschema, Authorize: AuthJWT = Depends()):
    user_dict=seeker.dict()
    adminColl.insert_one(user_dict)
    
    result = adminColl.find_one({"username":seeker.username,"email":seeker.email})
    if result:
        return{
            "status_code":200,
            "message":"registered succesfully"
              }

    else:
        
        return{
            "status_code":400,
            "message":"email already exists"   
        }
    
    

@app.post("/emailLogin")
def emailLogin(emailLogin:adminLoginSchema,response:Response, Authorize: AuthJWT = Depends()):
    existing_user = adminColl.find_one({"$and": [{"password": emailLogin.password}, {"email": emailLogin.email}]})


 
    if existing_user:

        token=Authorize.create_access_token(
            subject=str(existing_user['_id']),
            expires_time=timedelta(days=7),
            user_claims={
                "name":existing_user['email']
            }

        )
        return{
            "status_code":200,
            "message":"login succesful",
            "token":token
              }

    else:
        return{
            "status_code":400,
            "message":"invalid credentials"   
        }
@app.post("/forgotPassword")
async def forgotPassword(email: adminForgotPasswordSchema, Authorize: AuthJWT = Depends()):

        if email.email.split("@")[1] not in admin_allowed_domain:
            return HTTPException(status_code=403, detail={
                "status_code": 403,
                "message": "Forbidden Domain"
            })
        print(email)

        adminColl = mongoDBClient["adminCollection"]
        user = adminColl.find_one({"email": email.email})
        print(user)
        if user == None:
            return HTTPException(status_code=404, detail={
                "status_code": 404,
                "message": "Invalid Email"
            })

        otp = random.randint(100000, 999999)
        res = adminColl.update_one({"_id": user['_id']}, {
                                   "$set": {"mobileOtp": otp, "mobileOtpCreatedAt": datetime.now()}})
        
        print(user['email'])
        emailsent=sendmail(user['email'], "Things75","info@koneqto.com", "otp","you OTp for login is "+str(otp))
        
        print(emailsent)
        access_token = Authorize.create_access_token(subject=str(user['_id']),
                                                     user_claims={

            "type": "confidential",
            "otpVerified": False,
        
            "forgotPassword": True
        }
        )

        return HTTPException(status_code=200, detail={
            "status_code": 200,
            "message": "User found",
            "access_token": access_token

        })
@app.post("/resendSms")
async def resendSms(Authorize: AuthJWT = Depends()):
    # try:
        current_user = Authorize.get_jwt_subject()
        print(current_user)
        adminColl = mongoDBClient["adminCollection"]
        user = adminColl.find_one({"_id": ObjectId(current_user)})
        print(user)
        if user['mobileOtp'] != None:
            if (datetime.now() - user['mobileOtpCreatedAt']).seconds < 120:
                return HTTPException(status_code=401, detail={
                    "status_code": 401,
                    "message": "Wait for 2 minutes to resend OTP"
                })

        otp = random.randint(100000, 999999)
        res = adminColl.update_one({"_id": user['_id']}, {
                                   "$set": {"mobileOtp": otp, "mobileOtpCreatedAt": datetime.now()}})
        sendsms(user['mobile'], sendOtpTpl(otp))
        return HTTPException(status_code=200, detail={
            "status_code": 200,
            "message": "OTP resent successfully"
        })

    # seexcept:
    #     rai HTTPException(status_code=401, detail="Unauthorized")
@app.post("/verifyOtp")
def verifyOtp(otp: verifyOtpSchema, Authorize: AuthJWT = Depends()):
        current_user = Authorize.get_jwt_subject()
        claims = Authorize.get_raw_jwt()
        adminColl = mongoDBClient["adminCollection"]
        user = adminColl.find_one({"email":(otp.email)})
        print(user)
        if not user:
          raise HTTPException(status_code=404, detail={
            "status_code": 404,
            "message": "User not found"
        })
        if str(user.get('mobileOtp')) == str(otp.mobileOtp):
          raise HTTPException(status_code=401, detail={
            "status_code": 200,
            "message": "verified successfully"
        
        })
        print(user.get('mobileOtp'),str(otp.mobileOtp))
        if (user.get('mobileOtp')) != str(otp.mobileOtp):
          raise HTTPException(status_code=200, detail={
            "status_code": 200,
            "message": "invalid OTP"
        })

        if (datetime.now() - user.get('mobileOtpCreatedAt', datetime.min)).seconds > 300:
          raise HTTPException(status_code=401, detail={
            "status_code": 401,
            "message": "OTP expired"
        })

        # access_token = Authorize.create_access_token(subject=str(user['_id']),
        #                                              user_claims=claims,
        #                                              expires_time=timedelta(
        #                                                  minutes=300)
@app.post("/resetPassword")
async def reset_password(reset_data: adminPasswordSchema):
    email = reset_data.email
    new_password = reset_data.password
    user_data = adminColl.find_one({"email": email})

    if not user_data:

        return {

            "status_code": 404,

            "detail": "User not found"

        }
    # Update the user's password

    # hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    adminColl.update_one({"_id": user_data['_id']}, {"$set": {"password":new_password}})
    return {

        "status_code":202,

        "message": "Password reset successful"}

      

    
