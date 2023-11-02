import json
import pprint
import requests
import os

from requests import JSONDecodeError

from client_utils import hex_generator, get_user_data

"""
The client function sends "GET and "POST" requests to server and 
get answer from server
"""

url = "http://127.0.0.1:5000/list/"
current_path = os.path.abspath(os.getcwd())
log_file = os.path.join(current_path, 'results.log')


while True:
    # try:
    #     with open(log_file, mode="r", encoding="utf-8") as f:
    #         all_lines = f.readlines()
    #     for el in all_lines:
    #         print(el)
    # except FileNotFoundError:
    #     pass

    mode = input("[G]et or [P]ost or [Q]uit or lis[T] ? :  ")

    if mode == "Q":
        exit(0)

    elif mode == "T":
        url = "http://127.0.0.1:5000/list/"
        params = {'user_id': 'all' }
        response = requests.get(url, params=params)

        # Get response
        try:
            response_dict = json.loads(response.text)
            pprint.pprint(response_dict)
        except JSONDecodeError as e:
            print(e.response )



    elif mode == "G":
        url = "http://127.0.0.1:5000/list/"
        usr_id = input("Enter User_ID (or all) : ")

        params = {'user_id': usr_id }

        response = requests.get(url, params=params)

        # Get response
        try:
            response_dict = json.loads(response.text)
            pprint.pprint(response_dict)
        except JSONDecodeError as e:
            print(e.response)

    elif mode == "P":
        while True:
            key = input("[R]egistration | new_[M]essage | new_[P]ost | new_[L]ogin | rea[D] | Quit  : " )
            if key == "Q":
                break
            if key == "R":
                url = "http://127.0.0.1:5000/create/"
                user_id = hex_generator()
                notification_id = hex_generator()
                params = {
                    'user_id': user_id,
                    'notification_id': notification_id,
                    'key': "registration",
                }
                response = requests.post(url, data=params)
                print(f'user_id: {user_id}  Notification_id : {notification_id}')
                with open(log_file, mode="a", encoding="utf-8") as f:
                    f.write(f"user_id: {user_id} notification_id: {notification_id}  key: {key} \n")
                print(f"user_id:   {user_id}  notification_id:  {notification_id}   ")

                # Get response
                try:
                    response_dict = json.loads(response.text)
                    print(response_dict)
                except JSONDecodeError as e:
                    print(e.response)

            if key == "M":
                url = "http://127.0.0.1:5000/create/"
                user_data = get_user_data()
                pprint.pprint(user_data)
                user_id = input("message to user: ")
                inp_message = input("message : ")
                notification_id = hex_generator()
                params = {
                    'user_id': user_id,
                    'notification_id': notification_id,
                    'key': "new_message",
                    "data": inp_message
                }
                response = requests.post(url, data=params)
                pprint.pprint(params)
                # Get response
                response_dict = json.loads(response.text)
                print("\n")
                pprint.pprint(response_dict)
                with open(log_file, mode="a", encoding="utf-8") as f:
                    f.write(f"user_id: {user_id} notification_id: {notification_id}  key: {key} \n")

            if key == "P":
                url = "http://127.0.0.1:5000/create/"
                user_data = get_user_data()
                pprint.pprint(user_data)
                user_id = input("post to user: ")
                post_text = input("post_text : ")
                notification_id = hex_generator()
                params = {
                    'user_id': user_id,
                    'notification_id': notification_id,
                    'key': "new_post",
                    "data": post_text
                }
                response = requests.post(url, data=params)
                pprint.pprint(params)
                # Get response
                try:
                    response_dict = json.loads(response.text)
                    print("\n")
                    pprint.pprint(response_dict)
                    with open(log_file, mode="a", encoding="utf-8") as f:
                        f.write(f"user_id: {user_id} notification_id: {notification_id}  key: {key} \n")
                except JSONDecodeError as e:
                    print(e.response)


            if key == "L":
                url = "http://127.0.0.1:5000/create/"
                user_data = get_user_data()
                pprint.pprint(user_data)
                user_id = input("Login user: ")
                notification_id = hex_generator()
                params = {
                    'user_id': user_id,
                    'notification_id': notification_id,
                    'key': "new_login",
                    'data': "new login"
                }
                response = requests.post(url, data=params)
                pprint.pprint(params)
                # Get response
                response_dict = json.loads(response.text)
                print("\n")
                pprint.pprint(response_dict)
                with open(log_file, mode="a", encoding="utf-8") as f:
                    f.write(f"user_id: {user_id} notification_id: {notification_id}  key: {key} \n")

            if key == "D":
                url = "http://127.0.0.1:5000/read/"
                user_data = get_user_data()
                pprint.pprint(user_data)
                user_id = input("User id: ")
                notification_id = input("Notification ID : ")
                params = {
                    'user_id': user_id,
                    'notification_id': notification_id,
                    'key': "read",
                }
                response = requests.post(url, data=params)
                pprint.pprint(params)
                # Get response
                try:
                    response_dict = json.loads(response.text)
                    print("\n")
                    pprint.pprint(response_dict)
                    with open(log_file, mode="a", encoding="utf-8") as f:
                        f.write(f"user_id: {user_id} notification_id: {notification_id}  key: {key} \n")
                except JSONDecodeError as e:
                    print(e.response)

    else:
        continue
