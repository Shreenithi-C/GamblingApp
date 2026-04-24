import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

    def __str__(self):
        return f"DB Settings(host={self.DB_HOST}, user={self.DB_USER}, db={self.DB_NAME})"
