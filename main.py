'''small programm to check out intra42 api'''

import env
from check_out_user import check_out_user
from all_users import all_user_data

UID = env.uid
SECRET = env.secret
# API_URL = "https://api.intra.42.fr"


def main():
    '''main function'''

    all_user_data(UID, SECRET)


if __name__ == "__main__":
    main()
