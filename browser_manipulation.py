import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

class Browser:
    def __init__(self, driver:str):
        self.service = Service(driver)
        self.browser = webdriver.Firefox(service=self.service)

    def stop_voice(self):
        self.click_button(by=By.XPATH, value="//button[@aria-label='Disable Voice Output'][@type='button']")

    def open_page(self, url:str):
        self.browser.get(url)
        time.sleep(20)

    def close_browser(self):
        self.browser.close()

    def add_input(self, by: By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    def click_button(self, by: By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()

    def login(self, username: str, password: str):
        self.add_input(by=By.XPATH, value="//input[@type='text']", text=username)
        self.add_input(by=By.XPATH, value="//input[@type='password']", text=password)
        self.click_button(by=By.XPATH, value="//button[@type='submit']")
        time.sleep(15)
        #self.browser.maximize_window()
        #self.click_button(by=By.XPATH, value="//button[@aria-label='Expand'][@type='button']")

    def ask_question(self, question: str):
        self.add_input(by=By.CLASS_NAME, value="hTDBNO", text=question)
        self.click_button(by=By.XPATH, value="//button[@aria-label='Send Message'][@type='button']")

    def get_answer(self):
        time.sleep(20)
        answer = self.browser.find_element(By.CLASS_NAME, "kMDXqV")
        return answer

    def reset_chat(self):
        self.click_button(by=By.XPATH, value="//button[@aria-label='Clear Conversation'][@type='button']")
        time.sleep(1)
        self.click_button(by=By.XPATH, value="//button[@class='sc-fUnMCh dBUsUu'][@type='button']")
        time.sleep(2)


if __name__ == '__main__':
    browser = Browser('geckodriver.exe')











