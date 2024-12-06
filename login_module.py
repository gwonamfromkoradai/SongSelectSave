import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_cookies_and_token import get_cookie_and_token


def execute_login():
    driver = None
    try:
        # Step 1: Get the token and cookie
        print("Attempting to retrieve login token and cookies...")
        RequestVerificationToken, Cookie = get_cookie_and_token()

        if not Cookie:
            print("Login failed. No valid Cookie received.")
            return None  # Return None to indicate failure

        print("Login successful. Proceeding to launch the browser...")

        # Step 2: Launch the browser in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run browser in headless mode
        options.add_argument("--disable-gpu")  # Disable GPU (optional, improves stability)
        options.add_argument("--no-sandbox")  # Required in some environments
        options.add_argument("--window-size=1920,1080")  # Optional, set the browser window size
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        driver = webdriver.Chrome(options=options)

        # Step 3: Navigate to the root domain
        print("Navigating to https://ccli.com...")
        driver.get("https://ccli.com")

        # Step 4: Set cookies
        print("Setting cookies for the session...")
        cookies = Cookie.split("; ")  # Split cookie string into individual cookies
        for cookie in cookies:
            try:
                name, value = cookie.split("=", 1)
                driver.add_cookie({"name": name, "value": value, "domain": ".ccli.com"})
            except ValueError:
                print(f"Malformed cookie: {cookie}")
            except Exception as cookie_error:
                print(f"Error setting cookie: {cookie}. Error: {cookie_error}")

        # Step 5: Navigate to SongSelect
        print("Navigating to https://songselect.ccli.com...")
        driver.get("https://songselect.ccli.com")

        # Step 6: Verify login state
        WebDriverWait(driver, 10).until(EC.url_contains("songselect.ccli.com"))
        print("SongSelect opened successfully and logged in!")

        # Return the driver for reuse in the search GUI
        return driver

    except requests.RequestException as req_error:
        print(f"Request error during login: {req_error}")
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if not driver:
            print("Closing the browser due to error...")
            if driver:
                driver.quit()
