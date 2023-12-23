#!/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
from emailControl import emailSender

URL = "https://www.reg.uci.edu/perl/WebSoc"
department = "I&amp;C SCI"

driver = webdriver.Chrome()
driver.get(URL)

driver.find_element(by=By.NAME, value="Dept").send_keys(department)

driver.find_element(by=By.NAME, value="Submit").click()

driver.implicitly_wait(5)

pageSource = driver.page_source

soup = BeautifulSoup(pageSource, "html.parser")

classRows = soup.find_all("tr", bgcolor="#fff0ff")
data = soup.find_all("tr", bgcolor="#FFFFCC")

collected_count = 0

portfolio = {}
pattern = re.compile(r'\b\d{5}\b')
statusPattern = re.compile(r'\b(OPEN|FULL)\b')

for row in classRows:
    courseTitle = row.find_all(string=re.compile("\xa0 I&C Sci \xa0 33 \xa0 \xa0 "))

    if courseTitle:
        status = row.find_all_next("td")
        class_code = None
        class_status = None
        for td in status:
            class_code_matches = td.find_all(string=re.compile(pattern))
            if class_code_matches:
                class_code = class_code_matches[0]
            class_status_matches = td.find_all(string=re.compile(statusPattern))
            if class_status_matches:
                class_status = class_status_matches[0]
            
            if class_code and class_status:
                portfolio[class_code] = class_status
                class_code = None
                class_status = None

            collected_count += 1  # Increment the collected count
            if collected_count >= 171:  # Adjust the count based on your requirement
                break  # Stop collecting td elements when the count reaches the limit
            
for key, value in portfolio.items():
    if value == "OPEN":
        key_as_int = int(key)  # Convert key to integer for comparison
        if key_as_int >= 35622:
            emailSender({key})
        elif key_as_int == 35621 or key_as_int == 35620:
            emailSender({key})


