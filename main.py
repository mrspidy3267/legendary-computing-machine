# main.py
from seleniumbase import Driver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def check_display():
    """Verify that DISPLAY is properly set"""
    if "DISPLAY" not in os.environ:
        raise EnvironmentError("DISPLAY environment variable is not set")
    display = os.environ['DISPLAY']
    print(f"Using display: {display}")

def run_gitlab_automation():
    """
    Automate GitLab login process using SeleniumBase with undetected-chromedriver
    """
    driver = None
    try:
        # Verify display setup
        check_display()
        
        # Initialize the driver with undetected-chromedriver and additional options
        options = {
            "uc": True,
            "headless": True,
            "disable-gpu": True,
            "no-sandbox": True,
            "disable-dev-shm-usage": True
        }
        
        print("Initializing webdriver...")
        driver = Driver(**options)
        print("Webdriver initialized successfully")
        
        url = "https://gitlab.com/users/sign_in"
        print(f"Attempting to navigate to {url}")
        
        # Open URL with reconnect attempts
        max_attempts = 4
        for attempt in range(max_attempts):
            try:
                print(f"Connection attempt {attempt + 1} of {max_attempts}")
                driver.uc_open_with_reconnect(url, 4)
                print("Successfully connected to GitLab")
                break
            except WebDriverException as e:
                if attempt == max_attempts - 1:
                    print(f"Final attempt failed: {str(e)}")
                    raise e
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)

        # Handle captcha if present
        try:
            print("Checking for captcha...")
            driver.uc_gui_click_captcha()
            print("Captcha handled successfully")
        except Exception as e:
            print(f"Captcha handling error: {str(e)}")
            driver.save_screenshot("captcha_error.png")
            raise e

        # Wait for login form elements
        print("Waiting for login form elements...")
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "user_login"))
        )
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "user_password"))
        )
        print("Login form elements found")

        # Take a screenshot of successful loading
        print("Taking screenshot of login page...")
        driver.save_screenshot("gitlab_login_page.png")
        
        print("GitLab automation completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if driver:
            try:
                driver.save_screenshot("error_screenshot.png")
                print("Error screenshot saved")
            except Exception as screenshot_error:
                print(f"Failed to save error screenshot: {str(screenshot_error)}")
        raise e
        
    finally:
        if driver:
            print("Cleaning up webdriver...")
            driver.quit()
            print("Webdriver cleaned up successfully")

if __name__ == "__main__":
    print("Starting GitLab automation script...")
    run_gitlab_automation()
