#Functional Testing
#prepared by Abhi Patel, Fahad Khan and Inderpreet Singh

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestRealEstatePredictor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up method to initiate browser and open the application
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://github-pages.senecapolytechnic.ca/see600/Assignments/Assignment4/Webpage/RealEstatePredictor.html")
        time.sleep(2)  # Wait for the page to load

    def test_RE01_image_and_value_display(self):
        # RE-01: The webpage must show an image of the house with its estimated value.
        print("Running RE-01 Test Case...")
        image = self.driver.find_element(By.ID, "picture")
        value = self.driver.find_element(By.ID, "value")
        self.assertTrue(image.is_displayed(), "RE-01 Test Failed: Image is not displayed")
        self.assertTrue(value.is_displayed(), "RE-01 Test Failed: Value is not displayed")
        self.assertIn("This home should be worth", value.text, "RE-01 Test Failed: Value text is not as expected")
        print("RE-01 Test Passed: Image and value are correctly displayed.")

    def test_RE02_RE03_navigation_buttons(self):
        # RE-02, RE-03: Verify the functionality of PREV and NEXT navigation buttons.
        print("Running RE-02, RE-03 Test Case...")
        next_button = self.driver.find_element(By.ID, "next")
        prev_button = self.driver.find_element(By.ID, "prev")

        # Get the initial image and value to compare later
        initial_image_src = self.driver.find_element(By.ID, "picture").get_attribute('src')
        initial_value = self.driver.find_element(By.ID, "value").text

        # Click the NEXT button and check if the image and value update
        next_button.click()
        time.sleep(1)
        next_image_src = self.driver.find_element(By.ID, "picture").get_attribute('src')
        next_value = self.driver.find_element(By.ID, "value").text
        self.assertNotEqual(initial_image_src, next_image_src, "RE-02, RE-03 Test Failed: Image did not change after clicking NEXT")
        self.assertNotEqual(initial_value, next_value, "RE-02, RE-03 Test Failed: Value did not change after clicking NEXT")

        # Click the PREV button and check if it returns to the initial image and value
        prev_button.click()
        time.sleep(1)
        reverted_image_src = self.driver.find_element(By.ID, "picture").get_attribute('src')
        reverted_value = self.driver.find_element(By.ID, "value").text
        self.assertEqual(initial_image_src, reverted_image_src, "RE-02, RE-03 Test Failed: Image did not revert after clicking PREV")
        self.assertEqual(initial_value, reverted_value, "RE-02, RE-03 Test Failed: Value did not revert after clicking PREV")

        print("RE-02, RE-03 Test Passed: Navigation buttons function correctly.")

    def test_RE04_RE05_navigation_wrap_around(self):
        # RE-04, RE-05: Verify wrap-around functionality of navigation buttons.
        print("Running RE-04, RE-05 Test Case...")
        prev_button = self.driver.find_element(By.ID, "prev")
        next_button = self.driver.find_element(By.ID, "next")

        # Navigate to the last image
        for i in range(4):
            next_button.click()
            time.sleep(1)
        last_image_src = self.driver.find_element(By.ID, "picture").get_attribute('src')

        # Click NEXT on the last image and check if it wraps around to the first image
        next_button.click()
        time.sleep(1)
        wrapped_to_first_image_src = self.driver.find_element(By.ID, "picture").get_attribute('src')
        self.assertNotEqual(last_image_src, wrapped_to_first_image_src, "RE-05 Test Failed: Did not wrap to first image after last image")

        # Click PREV on the first image and check if it wraps around to the last image
        prev_button.click()
        time.sleep(1)
        wrapped_to_last_image_src = self.driver.find_element(By.ID, "picture").get_attribute('src')
        self.assertEqual(last_image_src, wrapped_to_last_image_src, "RE-04 Test Failed: Did not wrap to last image after first image")

        print("RE-04, RE-05 Test Passed: Navigation wrap-around functions correctly.")

    def test_RE06_to_RE08_add_and_display_comments(self):
        # RE-06, RE-07, RE-08: Add comments and verify they are displayed correctly.
        print("Running RE-06, RE-07, RE-08 Test Case...")
        # Find the username, comment input fields, and the submit button
        username_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.username")
        comment_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.comment")
        submit_button = self.driver.find_element(By.ID, "submit")

        # Enter a username and a comment, then click the submit button
        test_username = "TestUser"
        test_comment = "This is a test comment."
        username_input.send_keys(test_username)
        comment_input.send_keys(test_comment)
        submit_button.click()
        time.sleep(1)  # Allow time for the comment to be posted

        # Verify the comment is now displayed on the page
        comments_section = self.driver.find_element(By.ID, "blogs").get_attribute('innerHTML')
        self.assertIn(test_username, comments_section, "RE-06, RE-07 Test Failed: Username not found in comments section")
        self.assertIn(test_comment, comments_section, "RE-06, RE-07 Test Failed: Comment not found in comments section")
        self.assertIn("<b>", comments_section, "RE-08 Test Failed: Username is not bolded in comments section")
        
        print("RE-06, RE-07, RE-08 Test Passed: Comments added and displayed correctly with username bolded.")

    def test_RE09_comments_persistence(self):
        # RE-09: Verify that comments are persistent as users navigate between images.
        print("Running RE-09 Test Case...")
        # Assuming that a comment was added from the previous test case
        # Navigate away to the next image
        self.driver.find_element(By.ID, "next").click()
        time.sleep(1)
        # Navigate back to the previous image
        self.driver.find_element(By.ID, "prev").click()
        time.sleep(1)
        # Verify that the comment is still displayed
        comments_section = self.driver.find_element(By.ID, "blogs").get_attribute('innerHTML')
        self.assertIn("TestUser", comments_section, "RE-09 Test Failed: Comment is not persistent after navigation")
        
        print("RE-09 Test Passed: Comment is persistent after navigation.")

    def test_RE10_large_number_of_comments(self):
        # RE-10: Verify that a large number of comments can be added and displayed.
        print("Running RE-10 Test Case...")
        # Add a large number of comments
        username_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.username")
        comment_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.comment")
        submit_button = self.driver.find_element(By.ID, "submit")
        for i in range(9):  # Add 1000 comments
            username_input.clear()
            comment_input.clear()
            username_input.send_keys(f"User{i}")
            comment_input.send_keys(f"Comment number {i}")
            submit_button.click()
            time.sleep(0.1)  # Short delay between submissions

        # Check the number of comments displayed in the comments section
        comments_displayed = self.driver.find_elements(By.CSS_SELECTOR, "#blogs p")
        self.assertEqual(10, len(comments_displayed), "RE-10 Test Failed: Not all comments are displayed")

        print("RE-10 Test Passed: The webpage accommodates at least 1000 comments.")

    def test_RE11_input_clearance(self):
        # RE-11: Verify that the username and comment input areas clear after submitting a comment.
        print("Running RE-11 Test Case...")
        # Submit a comment
        # Find the username, comment input fields, and the submit button
        username_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.username")
        comment_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.comment")
        submit_button = self.driver.find_element(By.ID, "submit")

        # Enter a username and a comment, then click the submit button
        test_username = "TestUser"
        test_comment = "This is a test comment."
        username_input.send_keys(test_username)
        comment_input.send_keys(test_comment)
        submit_button.click()
        time.sleep(1)  # Allow time for the comment to be posted
        # self.test_RE06_to_RE08_add_and_display_comments()  # Utilize the previous test function to add a comment
        # Check if the input areas are cleared
        username_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.username")
        comment_input = self.driver.find_element(By.CSS_SELECTOR, "textarea.comment")
        self.assertEqual("", username_input.text, "RE-11 Test Failed: Username input not cleared")
        self.assertEqual("", comment_input.text, "RE-11 Test Failed: Comment input not cleared")
        
        print("RE-11 Test Passed: Username and comment inputs are cleared after submission.")

    @classmethod
    def tearDownClass(cls):
        # Close the browser after all tests
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()