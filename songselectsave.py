import pyperclip
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# Paths to save clipboard content
SAVE_FOLDER = "./songs"
FILE_PREFIX = "Clipboard_"

# Website to open
SONGSELECT_URL = "https://songselect.ccli.com/"

# Function to initialize the WebDriver
def initialize_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

# Function to extract song title
def extract_title(content):
    # Extract the first line as the title (adjust logic if needed)
    title_match = re.match(r"^[^\n\r]+", content.strip())
    if title_match:
        return title_match.group(0).strip()
    return None

# Function to save clipboard content
def save_clipboard_content(content):
    # Create the save folder if it doesn't exist
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    # Extract the title
    title = extract_title(content)
    if not title:
        title = FILE_PREFIX + time.strftime("%Y%m%d_%H%M%S")

    # Sanitize the title for use as a filename
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', title)

    # Generate the file path
    file_path = os.path.join(SAVE_FOLDER, f"{sanitized_title}.txt")

    # Save the content to the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Clipboard content saved to {file_path}")

# Function to monitor clipboard
def monitor_clipboard():
    print("Monitoring clipboard for changes. Press Ctrl+C to stop.")
    last_content = pyperclip.paste()  # Get the current clipboard content

    while True:
        try:
            # Get the current clipboard content
            current_content = pyperclip.paste()

            # Check if the content has changed
            if current_content != last_content:
                print("New clipboard content detected!")
                save_clipboard_content(current_content)
                last_content = current_content  # Update the last content

            time.sleep(1)  # Check the clipboard every second
        except KeyboardInterrupt:
            print("\nClipboard monitoring stopped.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

# Main function
def main():
    # Launch the browser to the SongSelect site
    try:
        driver = initialize_driver()
        driver.get(SONGSELECT_URL)
        print(f"Launched browser to {SONGSELECT_URL}")

        # Wait for the "Sign In" button and click it
        try:
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ProfileNavSignInLink"))
            )
            sign_in_button.click()
            print("Clicked the 'Sign In' button.")
        except Exception as e:
            print(f"Failed to find or click the 'Sign In' button: {e}")
    except Exception as e:
        print(f"Failed to launch browser: {e}")
        return

    # Start clipboard monitoring
    try:
        monitor_clipboard()
    except Exception as e:
        print(f"An error occurred during clipboard monitoring: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    main()
