import os
from dotenv import load_dotenv
load_dotenv()

_main = os.getenv("DATABASE_URL", "")
TEST_DB_URL = os.getenv("TEST_DATABASE_URL") or _main.rsplit("/", 1)[0] + "/socialpilot_test"