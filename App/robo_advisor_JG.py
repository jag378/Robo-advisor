#Initial Commit

import json
import os
import requests
import csv
import datetime

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

#Printing Names of All Stocks to be Printed
print("\n")
print("We will be collecting data on the following company tickers:")
print("****************************")

for stock in stocks_list:
    print(stock)

def dollar_format(value):
    return "${0:,.2f}".format(value)

def two_decimal_format(value):
    return "{0:.2f}".format(value)

#Gather Requests for Webpages

for stock in stocks_list:
    try:
        stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={my_api}"

        response = requests.get(stock_url)
        parsed_response = json.loads(response.text)

        #Making the Data More User-Friendly

        daily_prices = parsed_response["Time Series (Daily)"]

        #Dates Analysis

        dates = []

        for date in daily_prices:
            dates.append(date)


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

        #Save to CSV

        csv_filepath = os.path.join(os.path.dirname(__file__), "..", "data", stock + "_prices.csv")
        csv_headers = ["Time", "Open", "High", "Low", "Close", "Volume"]

        with open(csv_filepath, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()
            for prices in pricing_data:
                writer.writerow(prices)

        #Printing Calculations

        now = datetime.datetime.now()

        print("\n")
        print("Time of Lookup: " + str(now.strftime("%m/%d/%y %I:%M %p")))
        print("\n")
        print(stock + "'s VALUES AND CALCULATIONS:")

        recent_date = pricing_data[0]["Time"]
        print(stock + "'s Most Recent Closing Date: " + recent_date)

        latest_price = pricing_data[0]["Close"]
        latest_price_form = dollar_format(latest_price)
        print(stock + "'s Most Recent Closing Price: " + latest_price_form)

        daily_highs = []
        daily_lows = []

        for prices in pricing_data:
            daily_highs.append(prices["High"])

        recent_high = max(daily_highs)
        recent_high_form = dollar_format(recent_high)
        print(stock + "'s Recent Max High: " + recent_high_form)    

        for prices in pricing_data:
            daily_lows.append(prices["Low"])

        recent_low = min(daily_lows)
        recent_low_form = dollar_format(recent_low)
        print(stock + "'s Recent Min Low: " + recent_low_form)
        print("\n")

        #Stock Recommendation Data

        daily_closes = []
        for prices in pricing_data:
            daily_closes.append(prices["Close"])
        close_sum = sum(daily_closes)
        close_average = close_sum/len(daily_closes)
        

        volatility_index = ((recent_high - recent_low)/close_average)*100
        volatility_index_form = two_decimal_format(volatility_index)

        print(stock + " INVESTMENT STATISTICS:")
        print("This company has a volatility index of " + str(volatility_index_form) + "%")

        percent_of_delta = ((latest_price - recent_low) / (recent_high - recent_low)) * 100
        percent_of_delta_form = two_decimal_format(percent_of_delta)
        print("This company is trading at " + str(percent_of_delta_form) + "% of the delta between its recent high and recent low")
        print("\n")

        #Investment Decision
        print(stock + " COMPANY RECOMMENDATION:")

        if volatility_index < 20 and percent_of_delta < 40:
            print("This company is a STRONG BUY")
        elif volatility_index < 35 and percent_of_delta < 55:
            print("This company is a MODERATE BUY")
        elif volatility_index < 50 and percent_of_delta < 70:
            print("This company is a HOLD")
        elif volatility_index < 75 and percent_of_delta < 85:
            print("This company is a MODERATE SELL")
        else:
            print("This company is a STRONG SELL")
        
        print("\n")
        print("****************************")

    #Further Exploration / Challenges

        # Challenge 1: has been completed, as multiple inputs are already allowed

        # Challenge 2


    except KeyError:
        print("\n")
        print("Sorry! It appears " + stock +" doesn't correspond to a company!")




