import tkinter as tk
from tkinter import messagebox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

SAVE_FOLDER = "./songs"
FILE_PREFIX = "Song_"

class SongSelectApp:
    def __init__(self, root, driver):
        self.root = root
        self.root.title("SongSelect Automation")
        self.driver = driver  # Reuse the existing WebDriver instance
        self.song_links = []

        # Ensure the save folder exists
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)

        # Configure download folder
        self.configure_download_folder()

        # Create GUI elements
        self.create_widgets()

    def configure_download_folder(self):
        """Configure browser to download files into the desired folder."""
        params = {"behavior": "allow", "downloadPath": os.path.abspath(SAVE_FOLDER)}
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    def create_widgets(self):
        # Search Section
        self.search_label = tk.Label(self.root, text="Search for Songs:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.root, width=40)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search", command=self.perform_search)
        self.search_button.pack(pady=5)

        # Results Section
        self.results_label = tk.Label(self.root, text="Search Results:")
        self.results_label.pack()

        self.results_listbox = tk.Listbox(self.root, height=15, width=60)
        self.results_listbox.pack(pady=5)

        self.save_song_button = tk.Button(self.root, text="Save Song", command=self.save_song)
        self.save_song_button.pack(pady=5)

        # Reset Search
        self.reset_button = tk.Button(self.root, text="Reset Search", command=self.reset_search)
        self.reset_button.pack(pady=5)

        # Quit Application
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_application)
        self.quit_button.pack(pady=5)

    def perform_search(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Error", "Please enter a search query.")
            return

        try:
            print(f"Initiating search for: {query}")
            
            # Locate the search bar and enter the query
            search_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "SearchTextInput-1"))
            )
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys("\n")  # Simulate Enter key
            
            print("Waiting for search results to load...")
            
            # Wait for search results to appear
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "song-item"))
            )
            print("Search results loaded successfully!")
            self.display_search_results()
        except Exception as e:
            print("Error during search.")
            messagebox.showerror("Error", f"Failed to perform search: {e}")

    def display_search_results(self):
        try:
            songs = self.driver.find_elements(By.CLASS_NAME, "song-item")
            self.results_listbox.delete(0, tk.END)  # Clear previous results
            self.song_links.clear()  # Clear stored links

            for song in songs:
                try:
                    title = song.find_element(By.CLASS_NAME, "title").text
                    authors = song.find_element(By.CLASS_NAME, "authors").text
                    link = song.get_attribute("href")
                    self.results_listbox.insert(tk.END, f"{title} by {authors}")
                    self.song_links.append(link)  # Store link for navigation
                except Exception as e:
                    print(f"Error parsing song element: {e}")
        except Exception as e:
            print("Error retrieving search results.")
            messagebox.showerror("Error", f"Failed to retrieve search results: {e}")

    def save_song(self):
        try:
            selected_index = self.results_listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Error", "Please select a song.")
                return

            # Navigate to the lyrics page
            link = self.song_links[selected_index[0]]
            lyrics_link = link + "/viewlyrics"
            self.driver.get(lyrics_link)

            # Wait for the download button
            download_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "lyricsDownloadButton"))
            )
            download_button.click()  # Click the button to download the lyrics

            # Wait for the download to complete
            print("Downloading lyrics file...")
            time.sleep(5)  # Adjust this wait time as needed

            messagebox.showinfo("Status", "Song lyrics downloaded successfully.")

            # Automatically reset search after saving the song
            self.reset_search()
        except Exception as e:
            print(f"Error during song save: {e}")
            messagebox.showerror("Error", f"Failed to save song: {e}")

    def reset_search(self):
        """Reset the search fields and results."""
        self.search_entry.delete(0, tk.END)  # Clear search bar
        self.results_listbox.delete(0, tk.END)  # Clear search results
        self.song_links.clear()  # Clear stored song links
        print("Search reset successfully.")

    def quit_application(self):
        if self.driver:
            self.driver.quit()
        self.root.destroy()


if __name__ == "__main__":
    print("This script should not be run directly.")
