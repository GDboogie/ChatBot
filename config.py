import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve(strict=True).parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('POSTGRES_HOST')
DB_PORT = os.getenv('POSTGRES_PORT')
DB_NAME = os.getenv('POSTGRES_DB_NAME')
DATABASE: str = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
