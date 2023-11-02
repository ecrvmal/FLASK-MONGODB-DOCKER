"""
The main function receives "GET and "POST" requests from client and
send required information to client or write info to database
In some cases the script send e-mail to pre-configured email address.
"""

import os
import pprint
import time
from urllib import request

from flask import Flask,  json, request
from pymongo import MongoClient
from flask_restful import Api


from myapp.send_mail import send_email
from myapp.variables import *
from myapp.utils import arg_parser, hex_generator, request_data, note_normalization, logger, calc_items_new

# https://pymongo.readthedocs.io/en/stable/tutorial.html
# https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application
# https://www.geeksforgeeks.org/flask-http-methods-handle-get-post-requests/



app = Flask(__name__)
api = Api(app)

# client = MongoClient(DB_URI)                # works for IDE
client = MongoClient(DB_ALIAS, DB_PORT)   # works with Docker

db = client.flask_db
note = db.note

logger = logger()

# Response codes
RESPONSE_200 = app.response_class(response=json.dumps({"result": "success"}), status=201, mimetype='application/json')
RESPONSE_202 = app.response_class(response=json.dumps({"result": "success"}), status=202, mimetype='application/json')
RESPONSE_400 = app.response_class(response=json.dumps({"result": "Bad Request"}), status=400, mimetype='application/json')
RESPONSE_404 = app.response_class(response=json.dumps({"result": "User Not found"}), status=404, mimetype='application/json')
RESPONSE_500 = app.response_class(response=json.dumps({"fault": "Server fault"}), status=500, mimetype='application/json')
RESPONSE_501 = app.response_class(response=json.dumps({"fault": "user not exist"}), status=501, mimetype='application/json')
RESPONSE_502 = app.response_class(response=json.dumps({"fault": "user exist"}), status=502, mimetype='application/json')



def create_user(user_id, target_id):
    """
    The create_user function creates a new user in the database.
        Args:
            user_id (str): The ID of the new user to be created.
            target_id (str): The ID of the target that this new user will be associated with.

    :param user_id: Create a new user record in the database
    :param target_id: Create a new record for the user
    :return: The user_id
    :doc-author: Trelent
    """
    new_rec={
        'success': True,
        'data': {
            "elements": 1,
            "new": 1,
            "request": request_data(user_id, skip=0, limit=0 )
        },
        'list': [new_record(user_id, key="registration", target_id=target_id, data=""),],
    }
    note.insert_one(new_rec)
    return user_id


def get_note_by_userid(req_user_id):
    """
    The get_note_by_userid function takes a user_id as an argument and returns the note associated with that user_id.
        If no note is found, it returns False.

    :param req_user_id: Filter the notes by user_id
    :return: A note for the user with the specified id
    :doc-author: Trelent
    """
    # print(f'get_note_by_userid {req_user_id} \n' )
    users = list(note.find())
    if users:
        if req_user_id =="all":
            return users
        else:
            for el in users:
                # print(f'get_note_by_userid check  {el}\n')
                # print(el)
                if 'data' in el:
                    if 'request' in el['data']:
                        if 'user_id' in el['data']['request']:
                            if el['data']['request']['user_id'] == req_user_id:
                                # print(f'get_note_by_userid selected {el}\n' )
                                return el
    return False


def new_record(user_id, key, target_id="", data=""):

    """
    The new_record function creates a new record in the database.
        It takes three arguments: user_id, key, and target_id.
        The user_id is the id of the user who created this record.
        The key is a string that describes what kind of event this record represents (e.g., &quot;new-note&quot;).
        The target_id is an optional argument that specifies which object in our system was affected by this event (e.g., if we are creating a new note, then it would be the ID of that note).

    :param user_id: Identify the user who is making the request
    :param key: Specify the type of record
    :param target_id: Specify the id of the record that is being referenced
    :param data: Store the data of a record
    :return: A dictionary with the following keys:
    """
    new_rec ={
        "id": hex_generator(),
        "timestamp": time.time(),
        "is_new": True,
        "user_id": user_id,
        "key": key
    }
    if data:
        new_rec['data']=data
    if target_id:
        new_rec['target_id']=target_id
    # note.insert_one(new_rec)
    return new_rec

def update_items_new(note_obj):
    """
    The update_items_new function takes a note object as input and returns None.
    The function updates the 'data' field of the note object with two new fields:
    elements, which is a list of all items in the request, and new, which is a list
    of all items that are not yet in inventory. The function also removes any existing
    elements or new fields from data.

    :param note_obj: Access the note's data
    :return: None
    """
    items, items_new = calc_items_new(note_obj)
    newdata = {}
    # print(f'Update_items : note_obj: {note_obj}  items: {items}  items_new {items_new}')
    if '_id' in note_obj:
        note_id = note_obj['_id']
        if 'data' in note_obj:
            newdata['elements'] = items
            newdata['new'] = items_new
            newdata['request'] = note_obj['data']['request']
            db.note.update_one({'_id': note_id}, {'$set': {'data': newdata}}, upsert=False)
    return None


@app.route('/create/', methods=['POST'])
def create_notification():
    """
    The create_notification function is used to create a new notification record in the database.
        It takes POST data from the request and uses it to create a new notification record.
        The function returns RESPONSE_200 if successful, or one of several error codes otherwise.

    :return: A response object
    """
    data = request.form
    # print(f'got POST data: {data}')
    if 'user_id' in data:
        req_user_id = data['user_id']
    else:
        return RESPONSE_400
    if 'notification_id' in data:
        req_target_id = data['notification_id']
    else:
        req_target_id = ""
    if 'key' in data:
        req_key = data['key']
    else:
        return RESPONSE_400
    if 'data' in data:
        req_data = data['data']
    else:
        req_data = ""

    if req_key == "registration":
        logger.info(f"got registration request user_id: {req_user_id}, target_id: {req_target_id} key: {req_key}")
        if get_note_by_userid(req_user_id):
            return RESPONSE_502
        try:
            create_user(req_user_id, req_target_id)
            the_note = get_note_by_userid(req_user_id)
            update_items_new(the_note)
            send_email(subject="New Registration", message=f"user_id: {req_user_id}")
            logger.info(f"Registration request completed")
            return RESPONSE_200
        except Exception:
            logger.info(f"Registration request failed")
            return RESPONSE_500

    if req_key == "new_message":
        logger.info(f"got new_message request user_id: {req_user_id}, target_id: {req_target_id} key: {req_key}")
        the_note = get_note_by_userid(req_user_id)
        if not the_note:
            return RESPONSE_501
        try:
            note_id = the_note['_id']
            the_rec = new_record(req_user_id, req_key, target_id=req_target_id, data={"new message": req_data} )
            old_list = the_note['list']
            old_list.append(the_rec)
            db.note.update_one({'_id': note_id}, {'$set':{"list": old_list}}, upsert=False)
            update_items_new(the_note)
            # print(f"record with user_id: {req_user_id} updated with record_id: {req_target_id,}  key: {req_key} ")
            logger.info(f"Message request completed")
            return RESPONSE_200
        except Exception:
            logger.info(f"Message request failed")
            return RESPONSE_500

    if req_key == "new_post":
        logger.info(f"got new_post request user_id: {req_user_id}, target_id: {req_target_id} key: {req_key}")
        the_note = get_note_by_userid(req_user_id)
        if not the_note:
            return RESPONSE_501
        try:
            note_id = the_note['_id']
            the_rec = new_record(req_user_id, req_key, target_id=req_target_id, data={"new post": req_data} )
            old_list = the_note['list']
            old_list.append(the_rec)
            db.note.update_one({'_id': note_id}, {'$set':{"list": old_list}}, upsert=False)
            update_items_new(the_note)
            # print(f"record with user_id: {req_user_id} updated with record_id: {req_target_id,}  key: {req_key} ")
            logger.info(f"Post request completed")
            return RESPONSE_200
        except Exception:
            logger.info(f"Post request failed")
            return RESPONSE_500

    if req_key == "new_login":
        logger.info(f"got new_login request user_id: {req_user_id}, key: {req_key}")
        the_note = get_note_by_userid(req_user_id)
        if not the_note:
            return RESPONSE_501
        try:
            send_email(subject="New Login", message=f"New Login with ID: {req_user_id}")
            # print(f"mail sent with info user_id: {req_user_id} to: {EMAIL_TO} ")
            logger.info(f"Login request completed")
            return RESPONSE_200
        except Exception:
            logger.info(f"Login request failed")
            return RESPONSE_500


@app.route('/list/', methods=['GET'])
def notes_list():
    """
    The notes_list function returns a list of notes for the user_id provided in the request.
        The function takes two optional parameters: skip and limit.
        Skip is used to specify how many notes should be skipped before returning results,
        while limit specifies how many results should be returned after skipping.
    :return: A list of notes for a given user_id
    """
    if request.method == 'GET':

        # user_id = request.args.get('user_id')
        # print(request.args)
        user_id = request.args.get('user_id')
        skip = 0
        if request.args.get('skip'):
            skip = request.args.get('skip')
        limit = 0
        if request.args.get('limit'):
            limit = request.args.get('limit')
        logger.info(f"got LIST request user_id: {user_id} ")
        the_note = get_note_by_userid(user_id)
        # print(f'line 270 {the_note}')
        if not the_note:
            logger.info(f"Record list is empty ")
            return RESPONSE_200
        elif user_id == "all":
            result = []
            for el in the_note:
                update_items_new(el)
                result.append(note_normalization(el))
            response1 = app.response_class(
                response=json.dumps(result),
                status=200,
                mimetype='application/json'
            )
            logger.info(f"list request completed")
            return response1
        else:
            update_items_new(the_note)
            notes_lst = the_note['list']
            list_length = len(notes_lst)
            if skip and skip < list_length:
                notes_lst = notes_lst[skip:]
            list_length = len(notes_lst)
            if limit and limit < list_length:
                notes_list = notes_lst[:limit]
            the_note['list'] = notes_lst

            result = note_normalization(the_note)
            response1 = app.response_class(
                response=json.dumps(result),
                status=202,
                mimetype='application/json'
            )
            logger.info(f"list request completed")
            return response1


@app.route('/read/', methods=['POST'])
def read_notification():
    """
    The read_notification function is called when a user clicks on a notification.
    It takes in the user_id and notification_id of the clicked note, as well as an optional key parameter.
    If no key is provided, it defaults to &quot;read&quot;. The function then checks if there exists a note for that user_id.
    If not, it returns 501 (Not Implemented). If so, it iterates through all notifications in that list until
    it finds one with matching id's and sets its 'is_new' field to False.

    :return: Response_200 if the notification is successfully read,
    """
    data = request.form
    # print(f'got POST data: {data}')
    if 'user_id' in data:
        req_user_id = data['user_id']
    else:
        return RESPONSE_400
    if 'notification_id' in data:
        req_target_id = data['notification_id']
    else:
        req_target_id = ""
    if 'key' in data:
        req_key = data['key']
    else:
        return RESPONSE_400
    if req_key != "read":
        return RESPONSE_400

    logger.info(f"got READ request user_id: {req_user_id}, target_id: {req_target_id} key: {req_key}")
    if req_key == "read":
        the_note = get_note_by_userid(req_user_id)
        if not the_note:
            return RESPONSE_501
        note_id = the_note['_id']
        notes_list = the_note['list']
        for idx, el in enumerate(notes_list):
            if el['id'] == req_target_id:
                if 'is_new' in el:
                    if el['is_new'] == True:
                        notes_list[idx]['is_new'] = False
                        db.note.update_one({'_id': note_id}, {'$set': {"list": notes_list}}, upsert=False)
                        logger.info(f"READ request completed")
                        update_items_new(the_note)
                        return RESPONSE_200
        logger.info(f"READ request : record to update not found")
        return RESPONSE_200


if __name__ == '__main__':
    server_address, server_port = arg_parser()
    app.run(host='0.0.0.0', port=server_port, debug=True)




