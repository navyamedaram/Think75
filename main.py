from app.app import app
from app.Schemas import adminAuthSchema,workSpaceSchema,assesmentSchema,sectionSchema,questionSchema,adminSkillSchema,sponserSchema,servicesSchema,PaymentsSchema
# from app.Schemas.golbalSchemas import userStatusEnum
from app.controllers.admin import adminAuthController,adminDashboardController,adminWorkspaceController,uploadAssesmentController,sectionAuthController,questionAuthController,adminSkillController,sponserController,servicesController,PaymentsController
from fastapi.middleware.cors import CORSMiddleware
origins = ["https://koneqto.com/","http://localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
 )
