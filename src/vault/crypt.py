import os
import json
import pytz

from datetime import datetime
from cryptography.fernet import Fernet

from .utils import STORAGE, FORMAT

def _create_key():
    dt_created = datetime.now(tz=pytz.UTC)
    pw = Fernet.generate_key()

    fkey = Fernet.generate_key()
    enc_fkey = _encrypt(fkey, pw)

    data = {
        'key': enc_fkey.decode('utf8').replace("'", '"'),
        'key_dt_created': dt_created.strftime(FORMAT)
    }

    with open(STORAGE, 'w') as f: json.dump(data, f)
    return pw, dt_created

def get_key(pw):
    with open(STORAGE, 'r') as f: storage = json.load(f)
    enc_key = storage.get('key')
    key = _decrypt(enc_key, pw)
    return key

def _encrypt(data, key):
    f = Fernet(key)
    if isinstance(data, str): data = data.replace('"', "'").encode('utf8')
    enc_data = f.encrypt(data)
    return enc_data

def _decrypt(enc_data, key):
    f = Fernet(key)
    enc_data = enc_data.replace('"', "'").encode('utf8')
    data = f.decrypt(enc_data).decode('utf-8')
    return data
