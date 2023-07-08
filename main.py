import sys
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import subprocess
from env import uid, secret
import os

UID = uid
SECRET = secret
API_URL = "https://api.intra.42.fr"

def get_user_data(username):
    client = BackendApplicationClient(client_id=UID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=f"{API_URL}/oauth/token", client_id=UID, client_secret=SECRET)

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
        image = Image.open(image_response.raw)

        with open("profile_image.jpg", "wb") as f:
            image.save(f, "JPEG")

        subprocess.run(["imgcat", "profile_image.jpg"])
        
        os.remove("profile_image.jpg")
    else:
        print("Failed to retrieve the image.")

def main():
    if len(sys.argv) < 2:
        print("Please provide a username as an argument.")
        sys.exit(1)

    username = sys.argv[1]
    
    user_data = get_user_data(username)

    if user_data:
        image_url = user_data["image"]["versions"]["small"]

        display_profile_picture(image_url)

        print(user_data["location"])

if __name__ == "__main__":
    main()
