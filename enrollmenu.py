from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def pageSource():
    URL = "https://www.reg.uci.edu/registrar/soc/webreg.html"

    driver = webdriver.Chrome()
    driver.get(URL)

    driver.find_element(by=By.PARTIAL_LINK_TEXT, value="Access WebReg").click()
    driver.find_element(by=By.NAME, value="ucinetid").send_keys("sriyaj")
    driver.find_element(by=By.NAME, value="password").send_keys("Greendragonfly1!")
    driver.find_element(by=By.NAME, value="login_button").click()


if __name__ == "__main__":
    pageSource()