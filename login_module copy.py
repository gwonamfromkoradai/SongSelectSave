import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_cookies_and_token import get_cookie_and_token


def main():
    driver = None
    try:
        # Step 1: Get the token and cookie
        print("Attempting to retrieve login token and cookies...")
        RequestVerificationToken, Cookie = get_cookie_and_token()

        if not Cookie:
            print("Login failed. No valid Cookie received.")
            return

        print("Login successful. Proceeding to launch the browser...")

        # Step 2: Launch the browser
        options = webdriver.ChromeOptions()
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
            except Exception as cookie_error:
                print(f"Error setting cookie: {cookie}. Error: {cookie_error}")

        # Step 5: Navigate to SongSelect
        print("Navigating to https://songselect.ccli.com...")
        driver.get("https://songselect.ccli.com")

        # Step 6: Verify login state
        WebDriverWait(driver, 10).until(EC.url_contains("songselect.ccli.com"))
        print("SongSelect opened successfully and logged in!")

        # Step 7: Keep the browser open
        print("Browser will remain open. Press Enter in the terminal to exit...")
        input("Press Enter to close the browser and exit...")

    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if driver:
            print("Closing the browser...")
            driver.quit()


if __name__ == "__main__":
    main()
