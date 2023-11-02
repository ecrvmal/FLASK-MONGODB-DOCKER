import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from myapp.variables import ID_LENGTH


def hex_generator():

    """
    The hex_generator function generates a random hexadecimal string of length ID_LENGTH.
        The function uses the random module to select from a list of 16 characters,
        and then concatenates them together into one string.

    :return: A string of 6 hexadecimal digits
    :doc-author: Trelent
    """
    import random
    hex_digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    result = ""
    for digit in range(ID_LENGTH):
        cur_digit = random.choice(hex_digits)
        result += cur_digit
    print(result)
    return result


def get_user_data():

    """
    The get_user_data function reads the results.log file and returns a dictionary with the user's name as key and their score as value.

    :return: A dictionary with the user name as a key and the score as a value
    :doc-author: Trelent
    """
    result = {}
    with open("../results.log", mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    if lines:
        for line in lines:
                line = line.split(' ')
                result[line[0]] = line[2]
    return result



if __name__ == '__main__':
    print(hex_generator())