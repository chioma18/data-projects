from bs4 import BeautifulSoup
import requests

URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
PARAMETERS = {
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/102.0.0.0 Safari/537.36",
}


class DataManager:
    def __init__(self):
        response = requests.get(URL, headers=PARAMETERS)
        self.soup = BeautifulSoup(response.text, "html.parser")
        self.links = []
        self.prices = []
        self.addresses = []

    def get_listings_links(self):
        all_links = self.soup.find_all(name="a", class_="list-card-link")
        for link in all_links:
            if link['href'].startswith('/b'):
                link['href'] = 'https://zillow.com' + link['href']
                self.links.append(link['href'])
            else:
                self.links.append(link.get("href"))
        print(self.links)

    def get_prices(self):
        self.prices = [prices.getText() for prices in self.soup.find_all(class_="list-card-price")]
        for i in range(len(self.prices)):
            if self.prices[i].find("/mo") != -1:
                self.prices[i] = self.prices[i].replace("/mo", "")
            elif self.prices[i].find("+") != -1:
                self.prices[i] = self.prices[i].split("+")[0]
        print(self.prices)

    def get_addresses(self):
        self.addresses = [addresses.getText() for addresses in self.soup.find_all(class_="list-card-addr")]
        for i in range(len(self.addresses)):
            if self.addresses[i].find("|") != -1:
                self.addresses[i] = self.addresses[i].replace("|", "")
        print(self.addresses)


