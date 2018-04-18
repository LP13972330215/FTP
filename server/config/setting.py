import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)

DATABASE = os.path.join(BASE_DIR, "database")

HOME_PATH = os.path.join(BASE_DIR, "home")

USER_INFO = os.path.join(BASE_DIR, "config", "config.json")



