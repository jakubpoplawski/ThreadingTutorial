import random
import threading

import datetime
import time

import pathlib
from portability import resource_path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import requests
from bs4 import BeautifulSoup


class FinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super(FinancePriceScheduler, self).__init__(**kwargs)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.start()

    def run(self):
        while True:
            processed_value = self.input_queue.get()
            if processed_value == 'DONE':
                if self.output_queue is not None:
                    self.output_queue.put('None')
                break
            finance_worker = FinanceWorker(symbol=processed_value)
            retrieved_price = finance_worker.extract_price()
            if self.output_queue is not None:
                output_values = (processed_value,
                                 retrieved_price,
                                 datetime. datetime. now(datetime. UTC))
                self.output_queue.put(output_values)
            time.sleep(random.random())


class FinanceWorker():
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol.upper()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        self.url = f'https://finance.yahoo.com/quote/{self.symbol}/'

    def initialize_connection(self, user_agent):
        """The function creates a driver with applied user agent.

        Args:
            user_agent (str): Description of the user agent.
        """

        driverpath = pathlib.Path(resource_path('../ChromeDriver/chromedriver.exe'))

        chrome_options = Options()
       # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f"--user-agent={user_agent}")

        driver = webdriver.Chrome(service=Service(driverpath),
                                  options=chrome_options)

        return driver

    def click_refuse(self, driver, xpath_scrolldown_locator, xpath_button_locator):
        """The function clicks on the refuse cookies button when detected.

        Args:
            driver (obj): driver object driving the connection.
            xpath_scrolldown_locator (str): XPATH location of
            the scroll down button.
            xpath_button_locator (str): XPATH location of the button.
        """

        driver.execute_script("window.scrollTo(0, 2000);")
        try:
            WebDriverWait(
                driver, 3).until(EC.element_to_be_clickable((
                By.XPATH, xpath_scrolldown_locator))).click()
            WebDriverWait(
                driver, 3).until(EC.element_to_be_clickable((
                By.XPATH, xpath_button_locator))).click()
        except:
            pass

    def extract_price(self):
        driver = self.initialize_connection(self.user_agent)
        driver.get(self.url)
        self.click_refuse(driver,
                          '//*[@id="scroll-down-btn"]',
                          '//*[@class="btn secondary reject-all"]')
        read_price = driver.find_element(By.CSS_SELECTOR,
                                         '[class="livePrice yf-1i5aalm"]').text
        cleaned_price = read_price.replace(",", "")
        try:
            return float(cleaned_price)
        except ValueError:
            print('Caught value is not a number.')
