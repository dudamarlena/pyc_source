# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/jlogin/jlogin.py
# Compiled at: 2019-09-11 16:30:00
# Size of source mod 2**32: 3374 bytes
from os.path import dirname, realpath, join
from jlogin.utils.jlib import JsonManager
from getpass import getpass
from crypt import crypt
from hmac import compare_digest as hashEquals
from textwrap import dedent

class JLogin(JsonManager):

    def test(self):
        return 'oi'

    def __init__(self):
        self.root = dirname(realpath(__file__))
        self.path_data = join(self.root, 'data/data.json')

    def sign_in(self):
        print('### Sign In ###')
        username = input('Enter your username: ')
        password = getpass('Enter your password: ')
        password_verify = getpass('Repeat your password: ')
        while password != password_verify:
            print('Password do not match!')
            password_verify = getpass('Repeat your password: ')

        dirdata = join(self.root, 'data')
        JsonManager().create_json(self.path_data, dirdata, username, crypt(password_verify))
        print('Registration done!')

    def home(self, data):
        opc = '0'
        while opc != '2':
            print(dedent('\n            Menu:\n\n            1 - Alterar Login.\n            2 - Sair\n\n            Escolha uma opção:\n            '))
            opc = input('> ')
            if opc == '1':
                try:
                    self.update_login(data)
                except KeyboardInterrupt:
                    print('\nCancelado')

            elif opc == '2':
                break
            else:
                print('Option invalid!')

    def update_login(self, data):
        print('### Update Login ###')
        username = input('Enter new your username: ')
        password_old = getpass('Enter your old password: ')
        while not hashEquals(data['password'], crypt(password_old, data['password'])):
            print('Old password invalid!')
            password_old = getpass('Enter your old password: ')

        password_new = getpass('Enter your new password: ')
        password_new_repeat = getpass('Repeat new password: ')
        while password_new != password_new_repeat:
            print('New password do not match.')
            password_new_repeat = getpass('Repeat new password: ')

        data['username'] = username
        data['password'] = crypt(password_new_repeat)
        JsonManager().update_json(self.path_data, data)
        print('Update success!')

    def logging_in(self, data):
        print('### Logging In ###')
        username = input('Enter your username: ')
        while username != data['username']:
            print('Username invalid!')
            username = input('Enter your username: ')

        password = getpass('Enter your password: ')
        if not hashEquals(data['password'], crypt(password, data['password'])):
            print('Password invalid!')
        else:
            print('Login success!')
            self.home(data)

    def main(self):
        data = JsonManager().read_json(self.path_data)
        if data:
            try:
                self.logging_in(data)
            except KeyboardInterrupt:
                print('\nCancelado')

        else:
            try:
                self.sign_in()
            except KeyboardInterrupt:
                print('\nCancelado')

    def __str__(self):
        return self.main