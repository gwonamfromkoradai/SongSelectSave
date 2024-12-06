from login_module import execute_login
from search_save import SongSelectApp
import tkinter as tk

def main():
    print("Attempting login...")
    driver = execute_login()  # Login and return the driver

    print("Launching search and save GUI...")
    # Pass the driver to the search GUI
    root = tk.Tk()
    app = SongSelectApp(root, driver)
    root.mainloop()


if __name__ == "__main__":
    main()
