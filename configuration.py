import os

from dotenv import load_dotenv

load_dotenv()


ARANGO_HOST = os.getenv("ARANGO_HOST", "")
ARANGO_USERNAME = os.getenv("ARANGO_USERNAME", "")
ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD", "")
