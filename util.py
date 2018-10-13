import string
import random
import time
import os


def random_string(length=10):
    return ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=length))

def timestamp():
    return ''.join(time.strftime('%c').replace(':', '').split())

def append_timestamp_and_random_string(original_string):
    return f'{original_string}{timestamp()}{random_string()}'

def generate_unused_folder_path(prefix=''):
    while True:
        unused_folder_name = append_timestamp_and_random_string(prefix)
        if not os.path.isdir(unused_folder_name):
            return os.path.join(os.getcwd(), unused_folder_name)

def create_folder(path):
    os.mkdir(path)

def save_csv(csv, path, name):
    csv.save(os.path.join(path, f'{name}.csv')
