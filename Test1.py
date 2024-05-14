from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.python.org")
print(driver.title)
search_bar = driver.find_element(By.NAME, 'q')
search_bar.clear()
time.sleep(5)
search_bar.send_keys("getting started with python")
time.sleep(5)
search_bar.send_keys(Keys.RETURN)
print(driver.current_url)
time.sleep(10)
driver.close()