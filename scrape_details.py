import pandas as pd
import duckdb as db
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re

# set headless option to prevent browser window from opening
options = Options()
# options.add_argument('--headless')


SPILL_NUM = 9911471
driver = webdriver.Firefox(options=options)
driver.get("https://www.dec.ny.gov/cfmx/extapps/derexternal/index.cfm?pageid=2")
num_spill_field_elem = driver.find_element(By.NAME, 'spill_num')
num_spill_field_elem.clear() # Clear the input
num_spill_field_elem.send_keys(str(SPILL_NUM))
submit_elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/form[1]/div/input[4]')
submit_elem.click()
# driver.close()

page_html = driver.page_source
soup = BeautifulSoup(page_html, features='html.parser')
raw_values = [
    re.sub(
        '\n|\t', 
        '',
        tag.getText()
    ).replace('\xa0', ' ')
    for tag in soup.find_all('div', class_='indent')
]
print(raw_values)
    