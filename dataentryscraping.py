from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from data_manager import DataManager

CHROME_DRIVER_PATH = "C:\Development\chromedriver.exe"
URL = "https://docs.google.com/forms/d/e/1FAIpQLSecQWgu83_wAzrOzLKTYh1c0nCUGuN3jBujDtyEpyLMa7MhBw/viewform?usp=sf_link"

data_manager = DataManager()
data_manager.get_listings_links()
data_manager.get_prices()
data_manager.get_addresses()


class Form:
    def __init__(self, driver_path):
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service)

    def edit_form(self):
        self.driver.get(URL)
        self.driver.maximize_window()
        for i in range(0, 39):
            sleep(5)
            address_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address_input.send_keys(data_manager.addresses[i])

            sleep(2)
            price_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_input.send_keys(data_manager.prices[i])

            sleep(2)
            link_input = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_input.send_keys(data_manager.links[i])

            sleep(2)
            submit_button = self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit_button.send_keys(Keys.ENTER)

            sleep(5)
            sbt_another_response = self.driver.find_element(By.LINK_TEXT, "Submit another response")
            sbt_another_response.send_keys(Keys.ENTER)


form = Form(CHROME_DRIVER_PATH)
form.edit_form()

