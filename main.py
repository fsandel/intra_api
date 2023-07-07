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
    # Create an OAuth2 session using the client credentials
    client = BackendApplicationClient(client_id=UID)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=f"{API_URL}/oauth/token", client_id=UID, client_secret=SECRET)

    # Perform a GET request to /v2/users/{username}
    response = oauth.get(f"{API_URL}/v2/users/{username}")

    # Check the response status
    if response.status_code == 200:
        # Parse the response content as JSON
        data = response.json()
        return data
    else:
        print("Request failed with status:", response.status_code)
        return None

def display_profile_picture(image_url):
    # Retrieve the image data
    image_response = requests.get(image_url, stream=True)
    
    # Check the image response status
    if image_response.status_code == 200:
        # Save the image locally
        with open("profile_image.jpg", "wb") as f:
            f.write(image_response.content)
        
        # Display the image in the terminal using imgcat
        subprocess.run(["imgcat", "profile_image.jpg"])
        
        # Delete the image file
        os.remove("profile_image.jpg")
    else:
        print("Failed to retrieve the image.")

def main():
    # Retrieve the username from the command-line argument
    if len(sys.argv) < 2:
        print("Please provide a username as an argument.")
        sys.exit(1)

    username = sys.argv[1]
    
    # Get user data
    user_data = get_user_data(username)
    if user_data:
        # Access the medium version of the image URL
        image_url_medium = user_data["image"]["versions"]["medium"]
        
        # Display the profile picture
        display_profile_picture(image_url_medium)
        
        # Display the current location
        print(user_data["location"])

if __name__ == "__main__":
    main()
