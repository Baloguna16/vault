import json
import click

from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .crypt import get_key
from .crypt import _create_key, _encrypt, _decrypt

from .utils import STORAGE, MAX_ATTEMPTS
from .utils import set_cooldown, check_cooldown

@click.group()
def interface():
    """

    Welcome to my vault... No secrets here...

    This tool depends on you knowing at least one secret. Well? What is it..

    """

@click.command('init')
def init():
    click.echo('Welcome to the vault. Spinning up a password for you...')
    pw, dt_created = _create_key()
    click.echo(pw)

@click.command('encrypt')
@click.option('-l', '--label', help='Name of the resource you would like to lock')
@click.option('-d', '--data', help='The resource that you would like to lock')
def encrypt(label, data):
    with open(STORAGE, 'r') as f: storage = json.load(f)
    check_cooldown(storage)

    tries = 0
    while tries < MAX_ATTEMPTS:
        pw = input('Password: ')

        key = get_key(pw)
        if key is None:
            tries += 1
            continue

        enc_data = _encrypt(data, key)

        storage[hashed_label] = enc_data.decode('utf8')
        with open(STORAGE, 'w') as f: json.dump(storage, f)
        click.echo('Your resource has been stored in the vault!')
        return

    set_cooldown(storage)
    click.echo('Sorry, you ran out of tries...')

@click.command('decrypt')
@click.option('-l', '--label', help='Name of the resource you would like to retrieve')
def decrypt(label):
    with open(STORAGE, 'r') as f: storage = json.load(f)
    check_cooldown(storage)

    tries = 0
    while tries < MAX_ATTEMPTS:
        pw = input('Password: ')

        key = get_key(pw)
        if key is None:
            tries += 1
            continue

        enc_data = storage.get(label)
        if enc_data: data = _decrypt(enc_data, key)
        else: raise Exception('No data with that label in storage')

        click.echo(f'Your secret is... {data}')
        return

    set_cooldown(storage)
    click.echo('Sorry, you ran out of tries...')

interface.add_command(init)
interface.add_command(encrypt)
interface.add_command(decrypt)

if __name__ == '__main__':
    interface()
