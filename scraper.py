from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date, timedelta

# set headless option to prevent browser window from opening
options = Options()
# options.add_argument('--headless')

HISTORICAL_SEARCH_WINDOW = 25 # number of years on the past to collect data for

today = date.today()
latest_start_date = today - timedelta(days=3)
search_starts = [
    (latest_start_date - timedelta(days=i*365)).strftime('%m/%d/%Y') for i in range(0,HISTORICAL_SEARCH_WINDOW)
]
search_ends = [
    (latest_start_date - timedelta(days=i*365)).strftime('%m/%d/%Y') for i in range(1,HISTORICAL_SEARCH_WINDOW+1)
]
search_intervals = list(zip(search_ends, search_starts))


driver = webdriver.Firefox(options=options)
driver.get("https://www.dec.ny.gov/cfmx/extapps/derexternal/index.cfm?pageid=2")
from_date_elem = driver.find_element(By.NAME, "from_date")
from_date_elem.send_keys('value', '01/01/2022')
to_date_elem = driver.find_element(By.NAME, "to_date")
to_date_elem.send_keys('value', '01/01/2023')
submit_elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/form[2]/div[8]/input[1]')
submit_elem.send_keys(Keys.RETURN)
# driver.close()