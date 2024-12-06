import requests
from cookie_extractor import gui_login
import os


def get_cookie_and_token():

    try:
        # Read RequestVerificationToken from a file
        print("Attempting to get RequestVerificationToken and Cookie from file.")

        # check if file ReqyestVerificationToken.txt exists
        if not os.path.exists("RequestVerificationToken.txt") or not os.path.exists(
            "Cookie.txt"
        ):
            raise Exception(
                "File RequestVerificationToken.txt or Cookie.txt not found."
            )

        with open("RequestVerificationToken.txt", "r") as f:
            RequestVerificationToken = f.read()
            f.close()

        # Read Cookie from a file
        with open("Cookie.txt", "r") as f:
            Cookie = f.read()
            f.close()

        print("RequestVerificationToken and Cookie read from file.")

    except:
        print(
            "Unable to get RequestVerificationToken and Cookie from file. Will try to login manually."
        )
        RequestVerificationToken, Cookie = gui_login()

        if RequestVerificationToken == None or Cookie == None:
            print("Unable to login. Exiting.")
            exit()

        else:
            print(
                "RequestVerificationToken and Cookie obtained successfully. Saving them to file for quicker future access."
            )
            with open("RequestVerificationToken.txt", "w") as f:
                f.write(RequestVerificationToken)
                f.close()

            with open("Cookie.txt", "w") as f:
                f.write(Cookie)
                f.close()

    return RequestVerificationToken, Cookie
