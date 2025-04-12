import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "OXKTY0HKWWDUMEL8"
NEWS_API_KEY = "8e9c4ef00795462ab97071ff86773dac"
ACCOUNT_SID = "AC7b60e266eaa779d7e0e5889f1b48f752"
AUTH_TOKEN = "9ae01db67c46c1258a1aac51fde6836a"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
# e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_stock = data_list[0]
yesterday_close_price = float(yesterday_stock["4. close"])
print(yesterday_close_price)

# Get the day before yesterday's closing stock price
day_before_stock = data_list[1]
day_before_close_price = float(day_before_stock["4. close"])
print(day_before_close_price)

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(yesterday_close_price - day_before_close_price)
up_down = None
if difference > 0:
    up_down = "🔺 "
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and
# closing price the day before yesterday.
difference_percent = round(difference / yesterday_close_price * 100)
print(difference_percent)

# If TODO4 percentage is greater than 5 then print("Get News").
if difference_percent > 1:

    news_params = {
        "apiKey": NEWS_API_KEY,
        "qIntitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    # STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    # Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    two_articles = articles[:3]
    print(two_articles)
    # STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article = [
        f"{STOCK_NAME}: {up_down}{difference_percent}% \nHeadline:{article['title']} \nBrief:{article['description']}"
        for article in two_articles
    ]
    # Send each article as a separate message via Twilio.
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_='+19034032090',
            to='+2347083323196'
        )
        print(message.status)

# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required 
to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st,
near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required 
to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, 
near the height of the coronavirus market crash.
"""
