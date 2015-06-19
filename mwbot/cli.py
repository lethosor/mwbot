import argparse
import getpass
import sys
try:
    import readline
except ImportError:
    pass

import mwbot

class AbortInput(KeyboardInterrupt): pass

import __builtin__
_input = __builtin__.raw_input if hasattr(__builtin__, 'raw_input') else __builtin__.input

DEBUG = '--debug' in sys.argv

def input(prompt='', validate=lambda _: True):
    try:
        while True:
            x = _input(prompt)
            if validate(x):
                return x
    except KeyboardInterrupt:
        raise AbortInput

def prompt_yn(prompt='', default=None):
    options = 'y/n'
    if default == True:
        default = 'y'
        options = 'Y/n'
    elif default == False:
        default = 'n'
        options = 'y/N'
    while True:
        choice = input(prompt + ' [' + options + '] ').lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        elif default and not choice:
            return default

def prompt_new_user():
    print('Setting up new user (press Ctrl-C to abort)')
    url = input('Site URL: ', validate=len)
    site_id = input('Site ID: ', validate=len)
    username = input('Username: ', validate=len)
    pass1, pass2 = None, None
    while True:
        pass1 = getpass.getpass('Password: ')
        pass2 = getpass.getpass('Verify password: ')
        if pass1 == pass2:
            break
        print('Passwords do not match')
    creds = mwbot.cred.UserCreds('%s:%s' % (site_id, username), url, pass1)
    return creds

def log(fmt, *args):
    try:
        print(fmt % args)
    except TypeError:
        print('%s %r (String formatting failed)' % (fmt, args))

if DEBUG:
    debug = log
else:
    debug = lambda *_, **__: None

def new_parser(**kwargs):
    parser = argparse.ArgumentParser()
    if kwargs.get('user', True):
        parser.add_argument('--user',
            help='User',
            required=kwargs.get('require_user', False))
    if kwargs.get('debug', True):
        parser.add_argument('--debug', help='Enable debugging output',
            required=False, action='store_true')
    return parser
