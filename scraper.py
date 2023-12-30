from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from emailControl import emailSender

def get_page_source(url, department):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.find_element(by=By.NAME, value="Dept").send_keys(department)
    driver.find_element(by=By.NAME, value="Submit").click()
    driver.implicitly_wait(5)
    page_source = driver.page_source
    driver.quit()
    return page_source

def extract_course_info(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    class_rows = soup.find_all("tr", bgcolor="#fff0ff")
    return class_rows

def parse_course_data(class_rows):
    portfolio = {}
    collected_count = 0
    pattern = re.compile(r'\b\d{5}\b')
    status_pattern = re.compile(r'\b(OPEN|FULL)\b')

    for row in class_rows:
        course_title = row.find_all(string=re.compile("\xa0 I&C Sci \xa0 33 \xa0 \xa0 "))

        if course_title:
            status = row.find_all_next("td")
            class_code = None
            class_status = None
            for td in status:
                class_code_matches = td.find_all(string=re.compile(pattern))
                if class_code_matches:
                    class_code = class_code_matches[0]
                class_status_matches = td.find_all(string=re.compile(status_pattern))
                if class_status_matches:
                    class_status = class_status_matches[0]
                
                if class_code and class_status:
                    portfolio[class_code] = class_status
                    class_code = None
                    class_status = None

                collected_count += 1  
                if collected_count >= 171:  
                    break  
    return portfolio

def send_emails(portfolio):
    for key, value in portfolio.items():
        if value == "OPEN":
            key_as_int = int(key)  
            if key_as_int >= 35622:
                emailSender(f"LAB {key} OPEN")
            elif key_as_int == 35621 or key_as_int == 35620:
                emailSender(f"CLASS {key} OPEN")

if __name__ == "__main__":
    URL = "https://www.reg.uci.edu/perl/WebSoc"
    department = "I&amp;C SCI"

    page_source = get_page_source(URL, department)
    class_rows = extract_course_info(page_source)
    portfolio = parse_course_data(class_rows)
    send_emails(portfolio)
