import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

URL = "https://www.amazon.com/dp/B088NDL2G1?ref_=cm_sw_r_cp_ud_dp_1ZHJYTR5EEJYVBN5WZ4Y&th=1"
MY_EMAIL = "miypython@outlook.com"
PASSWORD = "yimtho@1"
headers = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/102.0.0.0 Safari/537.36",
}

response = requests.get(url=URL, headers=headers)
# print(response.text)

soup = BeautifulSoup(response.content, "lxml")
print(soup.prettify())

price_text = soup.find(name="span", class_="a-price a-text-price a-size-medium apexPriceToPay").get_text()
price = float(price_text.split("$")[1])

if price <= 7:
    with smtplib.SMTP("outlook.office365.com", 995) as connection:
        print("connected...")
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Amazon Price Alert!\n\n【Upgrade】 LED Wireless Mouse, Rechargeable Slim Silent Mouse"
                "2.4G Portable Mobile Optical Office Mouse with USB & Type-c Receiver, 3 Adjustable DPI for Notebook, "
                "PC, Laptop, Computer, Desktop (Black)\nhttps://www.amazon.com/dp/B088NDL2G1?"
                "ref_=cm_sw_r_cp_ud_dp_1ZHJYTR5EEJYVBN5WZ4Y&th=1"
        )
        connection.quit()
