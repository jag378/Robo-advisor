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

#Gather Requests for Webpages

for stock in stocks_list:

    stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={my_api}"

    response = requests.get(stock_url)
    parsed_response = json.loads(response.text)
    print(type(parsed_response))

    company_data = parsed_response["Meta Data"]
    print(company_data)

#Making the Data More User-Friendly

daily_prices = parsed_response["Time Series (Daily)"]
print(daily_prices)
print(type(daily_prices))