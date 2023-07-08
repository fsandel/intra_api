import sys
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import subprocess
from env import uid, secret
import os
from check_out_user import check_out_user

UID = uid
SECRET = secret
#API_URL = "https://api.intra.42.fr"


def main():
    check_out_user(UID, SECRET)

if __name__ == "__main__":
    main()
