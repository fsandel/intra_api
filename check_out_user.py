import sys
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import subprocess
from env import uid, secret
import os

def get_user_data(username, uid, secret):
    API_URL = "https://api.intra.42.fr"

    client = BackendApplicationClient(client_id=uid)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=f"{API_URL}/oauth/token", client_id=uid, client_secret=secret)

    response = oauth.get(f"{API_URL}/v2/users/{username}")

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Request failed with status:", response.status_code)
        return None

def display_profile_picture(image_url, width=None, height=None):
    image_response = requests.get(image_url, stream=True)

    if image_response.status_code == 200:
        with Image.open(image_response.raw) as image:
            with open("profile_image.jpg", "wb") as f:
                image.save(f, "JPEG")
            subprocess.run(["imgcat", "profile_image.jpg"])
            os.remove("profile_image.jpg")
    else:
        print("Failed to retrieve the image.")

def check_out_user(uid, secret):
    if len(sys.argv) < 2:
        print("Please provide a username as an argument.")
        sys.exit(1)

    username = sys.argv[1]
    user_data = get_user_data(username, uid, secret)

    if user_data:
        image_url = user_data["image"]["versions"]["small"]
        display_profile_picture(image_url)
        print(user_data["location"])