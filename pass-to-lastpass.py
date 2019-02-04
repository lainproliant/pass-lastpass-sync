#!/usr/bin/env python3
#------------------------------------------------------------------------------
# Sync passwords to my.1password.com as documents.
#------------------------------------------------------------------------------
import argparse
import json
import os
import subprocess
from tqdm import tqdm

PASSWORD_DIR = os.path.expanduser('~/.password-store')

#------------------------------------------------------------------------------
class Config:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--password-dir', default=PASSWORD_DIR)
        parser.add_argument('--overwrite', action='store_true')
        self.parser = parser
        self.overwrite = False

    def parse(self):
        self.parser.parse_args(namespace=self)
        return self

#------------------------------------------------------------------------------
def write_to_lastpass(name):
    pw = subprocess.check_output(['pass', name]).decode()
    subprocess.check_output(['lpass', 'add', '--non-interactive',
        '--notes', name],
        input=pw, text=True)

#------------------------------------------------------------------------------
def delete_from_lastpass(name):
    subprocess.check_output(['lpass', 'rm', name])

#------------------------------------------------------------------------------
def get_local_password_names(config):
    return [os.path.splitext(os.path.basename(x))[0]
            for x in os.listdir(config.password_dir) if x != '.gpg-id']

#------------------------------------------------------------------------------
def password_exists_in_lastpass(name):
    try:
        subprocess.check_output(['lpass', 'show', '--name', name])
        return True

    except subprocess.CalledProcessError:
        return False

#------------------------------------------------------------------------------
def main():
    config = Config().parse()

    password_names = get_local_password_names(config)

    for name in tqdm(password_names):
        if not password_exists_in_lastpass(name):
            write_to_lastpass(name)

        elif config.overwrite:
            delete_from_lastpass(name)
            write_to_lastpass(name)

#------------------------------------------------------------------------------
if __name__ == '__main__':
   main()
