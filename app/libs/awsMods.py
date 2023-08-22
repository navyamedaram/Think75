# create a function to generate upload url to s3 bucket

from boto3 import client
from botocore.client import Config
from app.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME, AWS_S3_BUCKET

def generate_upload_url(object_name, expiration=3600):
    try: 
        s3_client = client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,region_name=AWS_REGION_NAME, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, config=Config(signature_version='s3v4'))
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': AWS_S3_BUCKET,
                                                            'Key': object_name },
                                                    ExpiresIn=expiration)
        return response
    except Exception as e:
        print(e)
        return None

def sendEmail(email, otp):
    print("sending email",email)
    Client = client(
    'ses',
    region_name=AWS_REGION_NAME,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
    response = Client.send_email(
        Destination={
            'ToAddresses': [email],
        },
        
       
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data':  str(otp) ,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'You have successfully registered with SmartInternz'
            },
        },
        Source='info@smartinternz.com'
    )