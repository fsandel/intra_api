'''small programm to check out intra42 api'''

import env
from check_out_user import check_out_user

UID = env.uid
SECRET = env.secret
# API_URL = "https://api.intra.42.fr"


def main():
    '''main function'''
    check_out_user(UID, SECRET)


if __name__ == "__main__":
    main()
