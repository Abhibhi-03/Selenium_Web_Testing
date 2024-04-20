#prepared by Abhi Patel, Fahad Khan and Inderpreet Singh

#performance testing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def measure_page_load_time(url):
    with webdriver.Chrome() as driver:
        start_time = time.time()
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "next")))  # Assume 'next' is critical to consider the page loaded
        load_time = time.time() - start_time
        print(f"Initial Page Load Time: {load_time:.2f} seconds")
        return load_time

def measure_navigation_time(url):
    with webdriver.Chrome() as driver:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "next")))

        # Measure time to navigate using 'Next' button
        start_time = time.time()
        driver.find_element(By.ID, "next").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "picture")))  # Assuming the picture changes with navigation
        navigation_time = time.time() - start_time
        print(f"Navigation Time (Next): {navigation_time:.2f} seconds")

        # Measure time to navigate back using 'Prev' button
        start_time = time.time()
        driver.find_element(By.ID, "prev").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "picture")))  # Confirm navigation back
        navigation_back_time = time.time() - start_time
        print(f"Navigation Time (Prev): {navigation_back_time:.2f} seconds")

        return navigation_time, navigation_back_time

def measure_comment_submission_time(url):
    with webdriver.Chrome() as driver:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit")))

        # Find input elements
        username_input = driver.find_element(By.CLASS_NAME, 'username')
        comment_input = driver.find_element(By.CLASS_NAME, 'comment')
        submit_button = driver.find_element(By.ID, 'submit')

        # Measure comment submission time
        username_input.send_keys("TestUser")
        comment_input.send_keys("This is a test comment.")
        start_time = time.time()
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "blogs")))  # Wait for the comment to appear in the list
        comment_time = time.time() - start_time
        print(f"Comment Submission Time: {comment_time:.2f} seconds")

        return comment_time

# Example usage
url = "https://github-pages.senecapolytechnic.ca/see600/Assignments/Assignment4/Webpage/RealEstatePredictor.html"
measure_page_load_time(url)
measure_navigation_time(url)
measure_comment_submission_time(url)
