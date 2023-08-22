from pymongo import MongoClient
from fastapi_jwt_auth import AuthJWT
client = MongoClient("mongodb://localhost:27017/")
mongoDBClient = client["Things75"]
adminColl = mongoDBClient["adminCollection"]
workspaces_collection= mongoDBClient["WorkspaceCollection"]
collection=mongoDBClient["adminAssessmentModel"]
sectionCollection=mongoDBClient["SectionCollection"]
newQuestion_admin_collection = mongoDBClient["newQuestion_admin_collection"]
skills_collection = mongoDBClient["adminskillcollection"]
sponser_collection=mongoDBClient["SponserCollection"]
services_collection=mongoDBClient["ServicesCollection"]
payment_plans_collection=mongoDBClient["PaymentCollection"]