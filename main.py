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

def handle_captcha(driver):
    """Handle captcha using Selenium methods instead of PyAutoGUI"""
    try:
        print("Checking for captcha...")
        
        # Wait for and find the iframe if it exists
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            if "recaptcha" in iframe.get_attribute("src").lower():
                print("Found reCAPTCHA iframe")
                driver.switch_to.frame(iframe)
                
                # Wait for and click the checkbox
                wait = WebDriverWait(driver, 10)
                checkbox = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".recaptcha-checkbox-border"))
                )
                checkbox.click()
                print("Clicked reCAPTCHA checkbox")
                
                # Switch back to default content
                driver.switch_to.default_content()
                return True
                
        # No captcha found
        print("No captcha detected")
        return False
        
    except Exception as e:
        print(f"Captcha handling note: {str(e)}")
        return False

def run_gitlab_automation():
    """
    Automate GitLab login process using SeleniumBase with undetected-chromedriver
    """
    driver = None
    try:
        # Verify display setup
        check_display()
        
        print("Initializing webdriver...")
        # Initialize driver with correct SeleniumBase options
        driver = Driver(
            uc=True,  # Use undetected-chromedriver
            undetected=True,  # Enhance undetected mode
            headless=False,  # Set to false to avoid PyAutoGUI issues
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        print("Webdriver initialized successfully")
        
        # Set window size for consistent behavior
        driver.set_window_size(1920, 1080)
        
        url = "https://gitlab.com/users/sign_in"
        print(f"Attempting to navigate to {url}")
        
        # Open URL with reconnect attempts
        max_attempts = 4
        for attempt in range(max_attempts):
            try:
                print(f"Connection attempt {attempt + 1} of {max_attempts}")
                driver.get(url)  # Using standard get instead of uc_open_with_reconnect
                time.sleep(5)  # Wait for page to load completely
                print("Successfully connected to GitLab")
                break
            except WebDriverException as e:
                if attempt == max_attempts - 1:
                    print(f"Final attempt failed: {str(e)}")
                    raise e
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)

        # Handle captcha using Selenium methods
        handle_captcha(driver)

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
