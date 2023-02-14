from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date, timedelta

# set headless option to prevent browser window from opening
options = Options()
# options.add_argument('--headless')

HISTORICAL_SEARCH_WINDOW = 25 # number of years in the past to collect data for

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
from_date_elem = driver.find_element(By.NAME, "from_date") # Select the "from date" box
from_date_elem.clear() # Clear the input
driver.switch_to.alert.accept() # Accept the alert
to_date_elem = driver.find_element(By.NAME, "to_date") # Select the "to date" box
to_date_elem.clear() # Clear the input
driver.switch_to.alert.accept() # Accept the alert
from_date_elem.send_keys('01/01/2010') # Send the start date
to_date_elem.send_keys('01/01/2011') # Send the end date
submit_elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/form[2]/div[8]/input[1]')
submit_elem.click()
print(driver.current_url)
# driver.close()