#Initial Commit

import json
import os
import requests
import csv


#pip install python-dotenv through the command prompt
from dotenv import load_dotenv

print("Hello World")

load_dotenv()

my_api = os.environ.get("ALPHAVANTAGE_API_KEY")