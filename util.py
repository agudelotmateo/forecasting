import string
import random
import time
import os


def generate_unused_folder_path(prefix='static/'):
    while True:
        unused_folder_name = append_timestamp_and_random_string(prefix)
        if not os.path.isdir(unused_folder_name):
            return join_paths(os.getcwd(), unused_folder_name)

def append_timestamp_and_random_string(original_string):
    return f'{original_string}{timestamp()}{random_string()}'

def timestamp():
    return ''.join(time.strftime('%c').replace(':', '').split())

def random_string(length=10):
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=length))

def join_paths(first_path, second_path):
    return os.path.join(first_path, second_path)

def create_folder(path):
    os.mkdir(path)
