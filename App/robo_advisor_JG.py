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
    if len(stock_ticker) > 4:
        print("Oops! That isn't a valid stock symbol. Please input the stock's 3-4 digit ticker next time")
    else:
        stocks_counted = stocks_counted + 1
        stocks_list.append(stock_ticker)

print(stocks_list)

def dollar_format(value):
    return "${0:,.2f}".format(value)

#Gather Requests for Webpages

for stock in stocks_list:
    try:
        stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={my_api}"

        response = requests.get(stock_url)
        parsed_response = json.loads(response.text)
        print(type(parsed_response))

        company_data = parsed_response["Meta Data"]
        print(company_data)


        #Making the Data More User-Friendly

        daily_prices = parsed_response["Time Series (Daily)"]
        print(type(daily_prices))

        #Dates Analysis

        dates = []

        for date in daily_prices:
            dates.append(date)

        print(dates)

        #Pricing Data

        pricing_data = []

        for date in dates:
            prices = {"Time": date,
                    "Open": float(daily_prices[date]['1. open']),    
                    "High": float(daily_prices[date]['2. high']),
                    "Low": float(daily_prices[date]['3. low']),
                    "Close": float(daily_prices[date]['4. close']),
                    "Volume": float(daily_prices[date]['5. volume'])  
            }

            pricing_data.append(prices)

        print(pricing_data)
        print(type(pricing_data))

        #Save to CSV

        csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
        csv_headers = ["Time", "Open", "High", "Low", "Close", "Volume"]

        with open(csv_filepath, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()
            for prices in pricing_data:
                writer.writerow(prices)

        #Printing Calculations



        latest_price = pricing_data[0]["Close"]
        latest_price_form = dollar_format(latest_price)
        print(latest_price_form)

        daily_highs = []
        daily_lows = []

        for prices in pricing_data:
            daily_highs.append(prices["High"])

        recent_high = max(daily_highs)
        recent_high_form = dollar_format(recent_high)
        print(recent_high_form)    

        for prices in pricing_data:
            daily_lows.append(prices["Low"])

        recent_low = min(daily_lows)
        recent_low_form = dollar_format(recent_low)
        print(recent_low_form)

    except KeyError:
        print("\n")
        print("Sorry! It appears " + stock +" doesn't correspond to a company!")




