from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import environ as env
from details import TDC
from os import system
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TDCBot:
    def __init__(self, remark, plan, account, numbers):
        self.plan = plan
        self.remark = remark
        self.account = account
        self.total_created = 0
        self.nums = numbers
        self.failed = []

    def start(self):
        self.URL = f"https://erhvervselvbetjening.tdc.dk/account/{self.account}/ordernewmobile?action=order&project=mobil&lang=da&accountNo={self.account}"
        self.driver = self.setup_selenium_driver()
        self.driver.get(self.URL)
        system("cls")
        self.remove_cookies_request()
        self.login()
        self.create_subscriptions()

    def setup_selenium_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("log-level=3")
        options.add_argument("--silent")
        options.add_argument("start-maximized")
        driver = webdriver.Chrome("./chromedriver", options=options)
        return driver

    def create_subscriptions(self):
        for sub in self.nums:
            print(self.setup_subscription(sub, self.remark))

    def find_button(self, text):
        buttons = self.driver.find_elements_by_tag_name("button")
        result = list(filter(lambda x: x.get_attribute("innerHTML") == text, buttons))
        return None if not result else result[0]

    def remove_cookies_request(self):
        xpath = '//*[@id="coiPage-1"]/div[2]/div[1]/button[3]'
        accept_button = self.driver.find_element_by_xpath(xpath)
        if accept_button:
            accept_button.click()

    def login(self):
        self.driver.find_element_by_id("username").send_keys(TDC.EMAIL)
        self.driver.find_element_by_id("password").send_keys(TDC.PASSWORD)
        self.driver.find_element_by_id("post-button").click()

    def select_account(self):
        self.driver.get(self.URL)

    def complete_dropdown(self, id):
        sleep(1)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "Select"))
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(@id, '{id}')]"))
        ).click()

    def select_subscription_type(self, type):
        sleep(3)
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + Keys.HOME)
        self.complete_dropdown("--option-1")
        self.find_button("Videre").click()
        self.complete_dropdown(type)
        sleep(2)
        self.find_button("Videre").click()

    def fill_text_field(self, position, text):
        field = self.driver.find_elements_by_class_name("input-field__input")[position]
        field.click()
        field.send_keys(text)
        sleep(1)  # Fixing TDC check sometimes failing.
        field.send_keys(Keys.BACKSPACE)
        sleep(1)
        field.send_keys(text[-1])

    def report(self):
        if self.failed:
            print("List of failed SIM cards:")
            for each in self.failed:
                print(each)
        else:
            print("All SIM cards have been successfully created!")

    def setup_subscription(self, number, remark):
        self.select_account()
        self.select_subscription_type(self.plan)
        self.complete_dropdown("--option-2")
        sleep(3)
        self.fill_text_field(1, number)
        sleep(1)
        self.fill_text_field(2, remark)
        self.find_button("Videre").click()
        sleep(3)

        submit = self.find_button("Godkend")

        if not submit:
            self.failed.append(number)
            error = self.driver.find_element_by_class_name("input-field__status-msg")
            error_message = error.get_attribute("innerHTML")
            return f"{number} failed with error message: {error_message}"

        # submit.click()
        sleep(10)
        self.total_created += 1
        return f"{number} has been setup! {self.total_created}/{len(self.nums)}"
