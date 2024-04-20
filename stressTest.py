#prepared by Abhi Patel, Fahad Khan and Inderpreet Singh
#Stress Testing

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

def simulate_user_actions(user_id, num_actions):
    driver = webdriver.Chrome()
    driver.get('https://github-pages.senecapolytechnic.ca/see600/Assignments/Assignment4/Webpage/RealEstatePredictor.html')

    try:
        for action in range(num_actions):
            # Wait until the next button is clickable
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'next')))
            
            # Scroll into view and wait for any possible overlays to disappear
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)  # Adjust the sleep time if necessary to wait out any animations or overlays
            
            # Use Action Chains to avoid direct click intercepts
            ActionChains(driver).move_to_element(next_button).click().perform()

            # Wait for necessary elements for the next actions
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'username')))
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'comment')))
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'submit')))
            
            # Interaction with input elements
            username_input = driver.find_element(By.CLASS_NAME, 'username')
            comment_input = driver.find_element(By.CLASS_NAME, 'comment')
            submit_button = driver.find_element(By.ID, 'submit')

            username_input.clear()
            comment_input.clear()
            username_input.send_keys(f'User_{user_id}_Action_{action}')
            comment_input.send_keys(f'Comment for action {action} by User {user_id}')
            submit_button.click()

            # Optional: wait for the comment to appear or page to update
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'blogs')))

    finally:
        driver.quit()

    print(f'User {user_id} completed {num_actions} actions.')

# Example call to function
simulate_user_actions(0, 1000) #one sure, 1000 comments on different page
