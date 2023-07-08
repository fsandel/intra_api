'''module to check out userdata and print it to the terminal using intra42 api'''

import sys
import subprocess
import os
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image


def get_user_data(username, uid, secret):
    '''gets userdata from the given username, using given uid and secret'''

    api_url = "https://api.intra.42.fr"

    client = BackendApplicationClient(client_id=uid)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(
        token_url=f"{api_url}/oauth/token", client_id=uid, client_secret=secret)

    response = oauth.get(f"{api_url}/v2/users/{username}")

    if response.status_code == 200:
        data = response.json()
        return data

    print("Request failed with status:", response.status_code)
    return None


def display_profile_picture(image_url):
    '''displays the picture from the given url in the terminal'''

    image_response = requests.get(image_url, stream=True, timeout=5)

    if image_response.status_code == 200:
        with Image.open(image_response.raw) as image:
            with open("profile_image.jpg", "wb") as f:
                image.save(f, "JPEG")
            subprocess.run(["imgcat", "profile_image.jpg"], check=False)
            os.remove("profile_image.jpg")
    else:
        print("Failed to retrieve the image.")


def check_out_user(uid, secret):
    '''gets userdata and prints it the terminal'''

    if len(sys.argv) < 2:
        print("Please provide a username as an argument.")
        sys.exit(1)

    username = sys.argv[1]
    user_data = get_user_data(username, uid, secret)

    if user_data:
        image_url = user_data["image"]["versions"]["small"]
        display_profile_picture(image_url)
        print(user_data["location"])
