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

number_of_stocks = eval(input("How many stocks would you like data on?"))

stocks_counted = 0
stocks_list = []

while stocks_counted < number_of_stocks:
    stock_ticker = input("Please input a public company's stock ticker here: ")
    stocks_counted = stocks_counted + 1
    stocks_list.append(stock_ticker)

print(stocks_list)
