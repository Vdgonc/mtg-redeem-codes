import logging
from os import getenv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self):

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            filemode='w', filename='/tmp/mtg-redeem-code-browser.log')

        self.BINARY = '/usr/local/bin/chromedriver' if getenv(
            'CHROME_BINARY') is None else getenv('CHROME_BINARY')
        self.HEADLESS = None if getenv(
            'CHROME_HEADLESS') is None else '--headless'

        self.LOGIN_URL = 'https://myaccounts.wizards.com/login'
        self.ACCOUNT_URL = 'https://myaccounts.wizards.com/account'

        self.__errors = [
            'This code is not valid or has already been used the maximum amount of times for this account.']

        self.driver = self.get_driver()

    def get_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        if self.HEADLESS is not None:
            options.add_argument(self.HEADLESS)

        driver = webdriver.Chrome(self.BINARY, chrome_options=options)
        driver.implicitly_wait(10)

        return driver

    def __open_page(self, url):
        self.driver.get(url)

    def login(self, username, password):
        """Login to Wizards account

        Parameters:
            username (str): Wizards username
            password (str): Wizards password

        Returns:
            None

        """
        self.__open_page(self.LOGIN_URL)

        username_field = self.driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div/form/label[1]/input')
        password_field = self.driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div/form/label[2]/input')
        submit_button = self.driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div/form/button')

        username_field.send_keys(username)
        password_field.send_keys(password)
        logging.info('Logging in as {}'.format(username))
        submit_button.click()
        sleep(5)



    def redeem_code(self, code):
        """Redeem code

        Parameters:
            code (str): Code to redeem

        Returns:
            bool: True if code was redeemed, False if not
        """
        self.__open_page(self.ACCOUNT_URL)

        redeem_field = self.driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div/div[1]/form/label/input')
        logging.info('Redeeming code {}'.format(code))
        redeem_field.send_keys(code)
        redeem_field.send_keys(Keys.RETURN)

        sleep(10)

        message_field = self.driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div/div/div[1]/div')
        message_text = message_field.text

        logging.info('Validating code, message: {}'.format(message_text))
        if message_text in self.__errors:
            logging.info('Code {} was not redeemed'.format(code))
            return False

        logging.info('Code {} was redeemed'.format(code))
        return True

    def close_browser(self):
        self.driver.quit()
