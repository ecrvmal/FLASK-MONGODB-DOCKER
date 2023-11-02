import argparse
import sys

from variables import DEFAULT_SERVER_IP_ADDRESS, PORT, ID_LENGTH


def arg_parser():
    """
    the function for parsing command line
    :return:
    """
    '''
    Парсер аргументов командной строки, возвращает кортеж из 4 элементов
    адрес сервера, порт, имя пользователя, пароль.
    Выполняет проверку на корректность номера порта.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_SERVER_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=PORT, type=int, nargs='?')
    # parser.add_argument('-n', '--name', default=None, nargs='?')
    # parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    # client_name = namespace.name
    # client_passwd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        print(f'Incorrect port number: {server_port}. Correct addresses 1024.. 65535.')
        exit(1)

    return server_address, server_port


def reformat_doc(obj):
    obj['_id'] = str(obj['_id'])
    return obj


def hex_generator():
    import random
    hex_digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    result = ""
    for digit in range(ID_LENGTH):
        cur_digit = random.choice(hex_digits)
        result += cur_digit
    print(result)
    return result

def get_user_data():
    result = {}
    with open("../results.log", mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    if lines:
        for line in lines:
                line = line.split(' ')
                result[line[0]] = line[2]
    return result




def request_data(user_id, skip=0, limit=0 ):
    result = {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }
    return result


def note_normalization(note):
    print(f'note_normalization dict: {note}')
    if '_id' in note:
        note['id'] = note['_id'].__str__()
        # print(note['_id'].__dir__())
        note.pop('_id',None)
    if 'list' in note:
        for el in note['list']:
            if '_id' in el:
                el['id'] = el['_id'].__str__()
                el.pop('_id', None)
    return note


if __name__ == '__main__':
    print(hex_generator())