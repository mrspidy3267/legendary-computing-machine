# main.py
from seleniumbase import Driver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def run_gitlab_automation():
    """
    Automate GitLab login process using SeleniumBase with undetected-chromedriver
    """
    driver = None
    try:
        # Initialize the driver with undetected-chromedriver
        driver = Driver(uc=True)
        url = "https://gitlab.com/users/sign_in"
        
        # Open URL with reconnect attempts
        max_attempts = 4
        for attempt in range(max_attempts):
            try:
                driver.uc_open_with_reconnect(url, 4)
                break
            except WebDriverException as e:
                if attempt == max_attempts - 1:
                    raise e
                print(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(2)

        # Handle captcha if present
        try:
            driver.uc_gui_click_captcha()
        except Exception as e:
            print(f"Captcha handling error: {str(e)}")
            # Take screenshot if captcha handling fails
            driver.save_screenshot("captcha_error.png")
            raise e

        # Wait for login form elements to be present (example)
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "user_login"))
        )
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "user_password"))
        )

        # Add your login logic here if needed
        # username_field.send_keys(os.getenv("GITLAB_USERNAME"))
        # password_field.send_keys(os.getenv("GITLAB_PASSWORD"))
        
        # Take a screenshot of successful loading
        driver.save_screenshot("gitlab_login_page.png")
        
        print("GitLab automation completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        if driver:
            driver.save_screenshot("error_screenshot.png")
        raise e
        
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run_gitlab_automation()
