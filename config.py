from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQL_NAME_SERVER = os.getenv("SQL_NAME_SERVER")
    SQL_NAME = os.getenv("SQL_NAME")
    SQL_USER_NAME = os.getenv("SQL_USER_NAME")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD")

    AZURE_STORAGE_ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
    AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
    AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

    CLIENT_ID = os.getenv("CLIENT_ID")
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
    SCOPE = ["User.Read"]
    REDIRECT_URI = "http://localhost:5000/getAToken"

    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
