import os
import pytz
import json

from datetime import datetime, timedelta

FORMAT = '%Y-%m-%d-%H:%M:%S.%f'

STORAGE = os.getenv('STORAGE_FILE')
COOLDOWN = int(os.getenv('COOLDOWN_TIME'))
MAX_ATTEMPTS = int(os.getenv('MAX_ATTEMPTS'))

def check_cooldown(storage):
    if storage.get('is_on_cooldown') == True:
        dt_cooldown_str = storage.get('dt_cooldown')
        dt_cooldown = datetime.strptime(dt_cooldown_str, FORMAT)
        assert datetime.now() > dt_cooldown, 'Sorry, still on cooldown...'

        storage['is_on_cooldown'] = False
        storage['dt_cooldown'] = None
        with open(STORAGE, 'w') as f: json.dump(storage, f)

def set_cooldown(storage):
    """Failed attempts are penalized now"""

    dt_cooldown = datetime.now(tz=pytz.UTC) + timedelta(hours=COOLDOWN)

    storage['is_on_cooldown'] = True
    storage['dt_cooldown'] = dt_cooldown.strftime(FORMAT)

    with open(STORAGE, 'w') as f: json.dump(storage, f)
