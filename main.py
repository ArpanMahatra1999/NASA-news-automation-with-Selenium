# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# others
import pandas as pd
import time

# define driver
options = Options()
options.headless = True
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.nasa.gov/news/all-news/")

# define dataframe
df = pd.DataFrame()

# get containers
for i in range(3):
    containers = driver.find_elements(By.CLASS_NAME, "hds-content-item")
    for container in containers:
        title = container.find_element(By.CLASS_NAME, "hds-a11y-heading-22").text
        reading_time = int(container.find_element(By.CLASS_NAME, "hds-content-item-readtime").text.split()[0])
        description = container.find_element(By.XPATH, "./div[@class='hds-content-item-inner']/p").text
        url = container.find_element(By.XPATH, "./a").get_attribute('href')
        df = df.append({
            'title': title, 'reading time': reading_time, 'description': description, 'url': url
            }, ignore_index=True)
    print(df.tail(10))
    next_page = driver.find_element(By.CLASS_NAME, "next")
    driver.execute_script("arguments[0].click();", next_page)
    time.sleep(120)

# create df to csv file
df.to_csv("nasa.csv")

# close driver
driver.quit()