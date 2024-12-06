import tkinter as tk

VARIABLES_FILE = "variables.py"

def create_variables_file():
    """Prompt user for credentials and create variables.py."""
    def save_credentials():
        ccli_username = username_var.get().strip()
        ccli_password = password_var.get().strip()

        if not ccli_username or not ccli_password:
            print("Error: Both fields are required!")
            return

        with open(VARIABLES_FILE, "w") as file:
            file.write(f'ccli_userame = "{ccli_username}"\n')
            file.write(f'ccli_password = "{ccli_password}"\n')

        print("Success: Credentials saved successfully!")
        root.destroy()

    root = tk.Tk()
    root.title("Create Credentials")

    tk.Label(root, text="CCLI Username:").pack(pady=5)
    username_var = tk.StringVar()
    tk.Entry(root, textvariable=username_var, width=30).pack(pady=5)

    tk.Label(root, text="CCLI Password:").pack(pady=5)
    password_var = tk.StringVar()
    tk.Entry(root, textvariable=password_var, show="*", width=30).pack(pady=5)

    tk.Button(root, text="Save", command=save_credentials).pack(pady=10)

    root.mainloop()
