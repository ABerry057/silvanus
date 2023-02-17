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

today = date.today()
current_year = today.year
latest_start_date = (today - timedelta(days=3)).strftime('%m/%d/%Y')
all_years = range(1978, current_year-1)

intervals = [(f'01/01/{y}', f'01/01/{y+1}') for y in all_years]
intervals.append((f'01/01/{current_year}', latest_start_date))

# set up profile to handle downloads
cwd = pathlib.Path().absolute()
options.set_preference('browser.download.folderList', 2)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.download.dir', f'{cwd}/data/raw_data')
options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

driver = webdriver.Firefox(options=options)
progress_bar = tqdm(intervals)
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
    from_date = intervals[0]
    to_date = intervals[1]
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