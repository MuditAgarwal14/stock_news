import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv("E:/EnvironmentVariables/.env.txt")
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
PRICE_API_KEY = os.getenv("ALPHA_API_KEY")

date_time_object = datetime
current_date_and_time = date_time_object.now()
current_date = current_date_and_time.date()
yesterday_date = current_date - timedelta(1)
date_before_yesterday = current_date - timedelta(2)

price_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": PRICE_API_KEY,
}

price = requests.get("https://www.alphavantage.co/query", params=price_parameters)
price_before_yesterday = price.json()["Time Series (Daily)"][str(date_before_yesterday)]["4. close"]
price_yesterday = price.json()["Time Series (Daily)"][str(yesterday_date)]["4. close"]

change_in_price = round(((float(price_yesterday) - float(price_before_yesterday))/float(price_yesterday))*100, 2)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# except KeyError
news_parameters = {
    "q": COMPANY_NAME,
    "from": current_date,
    "apiKey": NEWS_API_KEY,
}

msg = []

news = requests.get("https://newsapi.org/v2/top-headlines", params=news_parameters)
total_articles = len(news.json()["articles"])

for n in range(total_articles):
    title = news.json()["articles"][n]["title"]
    description = news.json()["articles"][n]["description"]
    msg.append({"title": title, "description": description})

account_sid = "ACdc4f8e99d0c7b09a7036568ed1235bab"
auth_token = os.getenv("AUTH_TOKEN")
client = Client(account_sid, auth_token)

if change_in_price > 4 or change_in_price < -4:
    for news in range(len(msg)):
        if change_in_price > 0:
            message = client.messages.create(
                body=f"{STOCK}: 🔺 {change_in_price}%\n"
                     f"Headline: {msg[news]['title']}\n"
                     f"Brief: {msg[news]['description']}",
                from_="+16086023093",
                to=os.getenv("MY_NUMBER")
             )
        else:
            message = client.messages.create(
                body=f"{STOCK}: 🔻 {abs(change_in_price)}%\n"
                     f"Headline: {msg[news]['title']}\n"
                     f"Brief: {msg[news]['description']}",
                from_="+16086023093",
                to=os.getenv("MY_NUMBER")
            )
