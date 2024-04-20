#prepared by Abhi Patel, Fahad Khan and Inderpreet Singh
#Scalability testing
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

def user_actions(num_comments_per_page, url, results, index):
    driver = webdriver.Chrome()  # Initialize the WebDriver for Chrome
    try:
        driver.get(url)  # Open the URL in a browser window

        overall_start_time = time.time()  # Start timing for the overall test duration
        comment_submission_times = []  # List to hold comment submission times for averaging later

        for x in range(num_comments_per_page):
            # Prepare to submit a comment
            username_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'username')))
            comment_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'comment')))
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'submit')))

            username_input.clear()
            comment_input.clear()
            username_input.send_keys(f'TestUser_{index}_{x}')  # Input username
            comment_input.send_keys('This is a test comment')  # Input comment
            
            # Scroll the button into view and attempt to click
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)  # Wait for any floating overlays to disappear

            comment_start_time = time.time()  # Time measurement starts just before clicking submit
            try:
                submit_button.click()
            except WebDriverException:
                driver.execute_script("arguments[0].click();", submit_button)  # Fallback to JS click

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'blogs')))  # Wait for the comment to appear
            comment_end_time = time.time()
            comment_submission_times.append(comment_end_time - comment_start_time)  # Calculate the time taken to submit each comment

        overall_end_time = time.time()

        # Store results in the results list at the index specified for this thread
        results[index] = {
            'overall_time': overall_end_time - overall_start_time,
            'average_comment_time': sum(comment_submission_times) / len(comment_submission_times)
        }

        print(f"User {index} test completed successfully with average comment time {results[index]['average_comment_time']:.2f} s.")
    except Exception as e:
        print(f"An error occurred with user {index}: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after the test

# Continue with your setup for threads and execution as previously outlined


def simulate_users(num_users, num_comments_per_page, url):
    results = [None] * num_users  # Prepare a list to store results from each thread
    threads = []

    for i in range(num_users):
        # Create a thread for each user simulation
        thread = threading.Thread(target=user_actions, args=(num_comments_per_page, url, results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # Wait for all threads to finish

    return results

# Example usage
start_time = time.time()
url = "https://github-pages.senecapolytechnic.ca/see600/Assignments/Assignment4/Webpage/RealEstatePredictor.html"
num_users = 5
num_comments_per_page = 1000
print(f"Starting scalability test with {num_users} users each making {num_comments_per_page} comments.")
results = simulate_users(num_users, num_comments_per_page, url)  # Execute the test
end_time = time.time()
elapsed_time = end_time - start_time

hours = int(elapsed_time // 3600)  # Number of hours
minutes = int((elapsed_time % 3600) // 60)  # Number of minutes
seconds = elapsed_time % 60  # Remaining seconds

# Print the total elapsed time in hours, minutes, and seconds
print(f"Total time elapsed for the script to run: {hours} hours, {minutes} minutes, {seconds:.2f} seconds.")
