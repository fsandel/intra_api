'''module to check out userdata and print it to the terminal using intra42 api'''

import sys
import subprocess
import os
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import json


def get_user_data(uid, secret, page):
    '''gets userdata from the given username, using given uid and secret'''

    api_url = "https://api.intra.42.fr"
    request = f"/v2/campus/heilbronn/users?page={page}"


    client = BackendApplicationClient(client_id=uid)
    oauth = OAuth2Session(client=client)
    oauth.fetch_token(token_url=f"{api_url}/oauth/token", client_id=uid, client_secret=secret)

    response = oauth.get(f"{api_url}{request}")

    if response.status_code != 200:
        return None
    data = response.json()
    pretty = json.dumps(data, indent=4)
    if pretty.__len__() < 5:
        return None

    return pretty

def all_user_data(uid, secret):
    '''gets userdata and prints it the terminal'''

    page = 0
    user_data = True
    while user_data is not None:
        user_data = get_user_data(uid, secret, page)
        print(user_data)
        page += 1

