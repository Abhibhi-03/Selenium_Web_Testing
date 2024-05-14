from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://github-pages.senecapolytechnic.ca/see600/Selenium/Tests/Test2/TemperatureConverter.html")
print(driver.title)
tempF = driver.find_element(By.ID,'from')
tempF.clear()
tempF.send_keys(36)
time.sleep(5)
convert = driver.find_element(By.ID, 'convert')
convert.send_keys(Keys.RETURN)
time.sleep(5)
tempC = driver.find_element(By.ID,'to')
print(tempC.get_attribute('value'))

print(driver.current_url)
time.sleep(10)
driver.close()
