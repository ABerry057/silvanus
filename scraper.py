from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tqdm import tqdm
from datetime import date, timedelta
from time import sleep
import pathlib


# set headless option to prevent browser window from opening
options = Options()
options.add_argument('--headless')

# number of years in the past to collect data for
HISTORICAL_SEARCH_WINDOW = 10

today = date.today()
latest_start_date = today - timedelta(days=3)
search_starts = [
    (latest_start_date - timedelta(days=i*365)).strftime('%m/%d/%Y') for i in range(0,HISTORICAL_SEARCH_WINDOW)
]
search_ends = [
    (latest_start_date - timedelta(days=i*365)).strftime('%m/%d/%Y') for i in range(1,HISTORICAL_SEARCH_WINDOW+1)
]
search_intervals = list(zip(search_ends, search_starts))

# set up profile to handle downloads
cwd = pathlib.Path().absolute()
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', f'{cwd}/data/raw_data')
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

driver = webdriver.Firefox(options=options)
progress_bar = tqdm(search_intervals)
for interval in progress_bar:
    progress_bar_desc = 'Downloading year: ' + str(interval)
    progress_bar.set_postfix_str(progress_bar_desc)
    driver.get("https://www.dec.ny.gov/cfmx/extapps/derexternal/index.cfm?pageid=2")
    from_date_elem = driver.find_element(By.NAME, "from_date") # Select the "from date" box
    from_date_elem.clear() # Clear the input
    driver.switch_to.alert.accept() # Accept the alert
    to_date_elem = driver.find_element(By.NAME, "to_date") # Select the "to date" box
    to_date_elem.clear() # Clear the input
    driver.switch_to.alert.accept() # Accept the alert
    from_date = search_intervals[1]
    to_date = search_intervals[0]
    from_date_elem.send_keys(from_date) # Send the start date
    to_date_elem.send_keys(to_date) # Send the end date
    submit_elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/form[2]/div[8]/input[1]')
    submit_elem.click()
    # database search results page should now be loaded
    assert driver.title == 'Spill Incidents Database Search'
    export_csv_elem = driver.find_element(By.XPATH, '/html/body/div/div[3]/div/form/input[3]')
    sleep(3) # wait after each search to avoid throttling
    export_csv_elem.click()
driver.close()