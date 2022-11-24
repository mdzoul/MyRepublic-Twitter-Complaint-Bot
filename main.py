from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

PROMISED_DOWN = 300
PROMISED_UP = 300
TWITTER_EMAIL = os.environ.get('TWITTER_EMAIL')
TWITTER_PASSWORD = os.environ.get('TWITTER_PASSWORD')
TWITTER_USERNAME = 'MyRepublicUser'


class InternetSpeedTwitterBot:
    def __init__(self):
        self.s = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options, service=self.s)

        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get('https://www.speedtest.net/')
        self.driver.find_element(By.CSS_SELECTOR,
                                 '.start-button [aria-label="start speed test - connection type multi"]').click()
        time.sleep(60)
        down_speed = self.driver.find_element(By.CSS_SELECTOR,
                                              '[class="result-container-speed result-container-speed-active"] '
                                              '[class="result-data-large number result-data-value download-speed"]')
        up_speed = self.driver.find_element(By.CSS_SELECTOR,
                                            '[class="result-container-speed result-container-speed-active"] '
                                            '[class="result-data-large number result-data-value upload-speed"]')
        print(f"down: {down_speed.get_attribute('innerHTML')}")
        print(f"up: {up_speed.get_attribute('innerHTML')}")
        return float(down_speed.get_attribute('innerHTML')), float(up_speed.get_attribute('innerHTML'))

    def tweet_at_provider(self, down, up):
        self.driver.get('https://twitter.com/home')
        time.sleep(5)
        email_input = self.driver.find_element(By.NAME, 'text')
        email_input.send_keys(TWITTER_EMAIL)
        next_btn = self.driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
        next_btn[2].click()
        time.sleep(1)
        try:
            password_input = self.driver.find_element(By.NAME, 'password')
        except NoSuchElementException:
            username_input = self.driver.find_element(By.NAME, 'text')
            username_input.send_keys(TWITTER_USERNAME)
            time.sleep(1)
            next_btn = self.driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
            next_btn[1].click()
            time.sleep(1)
            password_input = self.driver.find_element(By.NAME, 'password')
            password_input.send_keys(TWITTER_PASSWORD)
            time.sleep(1)
            login_btn = self.driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
            login_btn[3].click()
            time.sleep(3)
        else:
            password_input.send_keys(TWITTER_PASSWORD)
            time.sleep(1)
            login_btn = self.driver.find_elements(By.CSS_SELECTOR, '[role="button"]')
            login_btn[3].click()
            time.sleep(3)
        tweet_text = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Tweet text"]')
        tweet_text.send_keys(f'Hey @MyRepublicSG, why is my internet speed {down}down/{up}up '
                             f'when I pay for GAMER 1Gbps in Singapore? #speedtest ')
        tweet = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')
        tweet.click()


bot = InternetSpeedTwitterBot()
down, up = bot.get_internet_speed()
if down < PROMISED_DOWN and up < PROMISED_UP:
    bot.tweet_at_provider(down, up)
else:
    print("Internet speed is satisfactory")

bot.driver.quit()
