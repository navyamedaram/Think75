from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT


class Settings(BaseModel):
    "Settings"
    authjwt_secret_key: str = "secret"

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    "Hello World"
    return Settings()