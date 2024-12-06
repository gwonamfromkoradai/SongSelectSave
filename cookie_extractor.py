from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import variables
import requests
import time
import random

# Add your login credentials here
email = variables.ccli_userame
password = variables.ccli_password

# Start Chrome with logging preferences for performance (network events only)
options = webdriver.ChromeOptions()
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Variables to store the token and cookie
request_verification_token = None
required_cookies_dict = {}

required_cookies = [
    "ARRAffinity",
    "ARRAffinitySameSite",
    "CCLI_AUTH",
    "CCLI_JWT_AUTH",
    ".AspNetCore.Session",
]
antiforgery_cookie_prefix = ".AspNetCore.Antiforgery"


def report_first_song():
    try:
        # Wait for the "Report Song" button to become clickable
        report_song_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(span/text(),'Report Song')]")
            )
        )
        report_song_button.click()

    except Exception as e:
        print(
            "Unable to automatically report the first song.\n Please try clicking the 'Report Song' button manually, to report any song."
        )


def capture_post_requests(logs):
    global request_verification_token

    for entry in logs:
        log = json.loads(entry["message"])["message"]

        if (
            log["method"] == "Network.requestWillBeSent"
            and log["params"]["request"]["method"] == "POST"
        ):
            headers = log["params"]["request"]["headers"]

            if "RequestVerificationToken" in headers:
                request_verification_token = headers["RequestVerificationToken"]
                cookies = driver.get_cookies()
                if are_cookies_captured(cookies):
                    print("Cookies Captured")
                    required_cookies_dict.update(extract_required_cookies(cookies))
                return True
    return False


def are_cookies_captured(cookies):
    cookie_names = [cookie["name"] for cookie in cookies]
    for required_cookie in required_cookies:
        if required_cookie not in cookie_names:
            return False
    if not any(
        cookie["name"].startswith(antiforgery_cookie_prefix) for cookie in cookies
    ):
        return False
    return True


def extract_required_cookies(cookies):
    cookies_dict = {}
    for cookie in cookies:
        cookie_name = cookie["name"]
        cookie_value = cookie["value"]
        # Check if the cookie name matches the required cookies
        if cookie_name in required_cookies:
            cookies_dict[cookie_name] = cookie_value
        # Handle antiforgery cookies
        if cookie_name.startswith(antiforgery_cookie_prefix):
            cookies_dict[cookie_name] = cookie_value
    return cookies_dict


def handle_cookie_popup():
    try:
        # Check if the cookie popup is displayed
        cookie_popup = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "CybotCookiebotDialog"))
        )
        if cookie_popup:
            # Click the "Allow all" button
            allow_all_button = driver.find_element(
                By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"
            )
            allow_all_button.click()
            # print("Cookie popup closed.")
            # wait 2 seconds for the popup to close
            WebDriverWait(driver, 2).until_not(
                EC.visibility_of_element_located((By.ID, "CybotCookiebotDialog"))
            )
    except Exception as e:
        print("Cookie popup not found or already handled.")
        pass


def getVerificationToken(cookies):

    print("Attempting to get verification token...")

    # Define the URL
    url = "https://reporting.ccli.com/api/antiForgery"

    # Define the headers from the raw capture
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://reporting.ccli.com/",
        "Content-Type": "application/json;charset=utf-8",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
    }

    # Define the cookies from the raw capture
    cookies = cookies

    # Send the GET request
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
    except Exception as e:
        print(f"Error: {e}")
        return None

    if response.status_code == 200:
        return response.text.strip('"')
    else:
        print("Error getting verification token")
        return None


def gui_login():
    global driver  # Declare driver as global
    driver = webdriver.Chrome(options=options)
    driver.get("https://reporting.ccli.com/search")

    try:

        handle_cookie_popup()

        # Wait for redirect to login page
        WebDriverWait(driver, 20).until(
            EC.url_contains("profile.ccli.com/account/signin")
        )

        # Automatically fill in email and password
        email_field = driver.find_element(By.ID, "EmailAddress")
        password_field = driver.find_element(By.ID, "Password")

        email_field.send_keys(email)
        # pause 2 seconds
        time.sleep(2)

        # type the password key-by-key to try to trick the bot detection
        for letter in password:
            password_field.send_keys(letter)
            # wait random time between 0.1 and 0.3 seconds
            time.sleep(random.uniform(0.1, 0.3))

        # Click the login button
        login_button = driver.find_element(By.ID, "sign-in")
        login_button.click()

        # Wait until redirected back to the desired page
        WebDriverWait(driver, 20).until(EC.url_contains("reporting.ccli.com/search"))

        cookies = []
        while True:

            cookies = driver.get_cookies()
            time.sleep(5)  # Adjust the interval if necessary

            # Check if we have all required cookies
            if are_cookies_captured(cookies):
                print("All required cookies captured!")
                break
            else:
                print("Still waiting for all cookies...")

        # Filter and print only the required cookies
        filtered_cookies = extract_required_cookies(cookies)
        # for cookie_name, cookie_value in filtered_cookies.items():
        #     print(f"Cookie Name: {cookie_name}, Value: {cookie_value}")

        # Get the verification token
        request_verification_token = getVerificationToken(filtered_cookies)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    cookie_string = (
        "; ".join([f"{name}={value}" for name, value in filtered_cookies.items()]) + ";"
    )

    result = (request_verification_token, cookie_string)
    return result


if __name__ == "__main__":
    gui_login()
