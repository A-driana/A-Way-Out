from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    auth_jwt_secret_key: str
    sender: str
    rec: str
    pswd: str

    class Config:
        env_file = ".env"


settings = Settings()
