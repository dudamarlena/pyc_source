# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Komurasaki/.anyenv/envs/pyenv/versions/2.7.6/lib/python2.7/site-packages/src/pass_manager.py
# Compiled at: 2014-09-10 00:53:09
""" Simple CLI password manager
"""
import hashlib, cPickle as pickle, os
from argparse import ArgumentParser
from random import randint, choice
import subprocess, getpass
from encrypter import Encrypter
from collections import defaultdict
import json

class PasswordManager(object):
    """ Simple CLI Password Manager Tool developed by python"""
    PASS_FILE = ('{home}/.pass-manager.db').format(home=os.environ['HOME'])

    def __init__(self):
        """ if not db file, create new db file
        """
        self.encrypter = Encrypter()
        if os.path.exists(self.PASS_FILE):
            try:
                with open(self.PASS_FILE, 'r') as (f):
                    file_content = pickle.load(f)
                    if type(file_content) in (dict, defaultdict):
                        self.passwds = file_content
                    elif type(file_content) == str:
                        decrypted_file_content = self.encrypter.decrypt(file_content)
                        self.passwds = json.loads(decrypted_file_content)
                    else:
                        raise Exception('Unknown error...')
            except Exception as e:
                print 'failed loading db file... ', e
                os.remove(self.PASS_FILE)
                raise Exception('try it again.')

            master = self.passwds['master']
        else:
            self.passwds = {}
            master = getpass.getpass('This is your first time. Please input your master password => ')
            master = hashlib.sha256(master).hexdigest()
            self.passwds['master'] = master
            self._save_db()
        self.sha = hashlib.sha256(master)

    def _save_db(self):
        """ save or update db file
        """
        try:
            with open(self.PASS_FILE, 'w') as (f):
                json_passwds = json.dumps(self.passwds)
                encrypted_file_content = self.encrypter.encrypt(json_passwds)
                pickle.dump(encrypted_file_content, f)
        except Exception as e:
            raise Exception(('failed saving db file :{e}').format(e=e))

    def setpb_data(self, data):
        """ save password into clipboard
        """
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.communicate(data)

    def passwd_generator(self, salt):
        """ generate new password using master password and salt
        """
        self.sha.update(salt)
        digest = self.sha.hexdigest()[-12:]
        return self.passwd_strengthen(digest)

    def passwd_strengthen(self, digest):
        """ strengthen generated password
        """
        strengthened_digest = []
        signs = [
         '#', '$', '-', '=', '?', '@', '[', ']', '_']
        for c in digest:
            odd = randint(1, 10) % 2 == 1
            if c.isalpha() and odd:
                c = c.upper()
            elif c.isdigit() and not odd:
                sign = choice(signs)
                c = sign
            strengthened_digest.append(c)

        return ('').join(strengthened_digest)

    def save_passwd(self, salt, passwd):
        """ save generated and strengthened password with salt as key
        """
        if self.passwds.has_key(salt):
            to_overwrite = ''
            while to_overwrite not in ('y', 'n'):
                to_overwrite = raw_input('Overwrite? (y or n)')

            if to_overwrite == 'n':
                return False
        self.passwds[salt] = passwd
        self._save_db()
        return True

    def confirm_master(self):
        """ do auth by master password
        """
        valid_master = getpass.getpass('Please input master password => ')
        if valid_master == self.passwds['master']:
            master = hashlib.sha256(self.passwds['master']).hexdigest()
            self.passwds['master'] = master
            self._save_db()
        valid_master = hashlib.sha256(valid_master).hexdigest()
        if valid_master == self.passwds['master']:
            return True
        else:
            return False

    def show_passwds(self):
        """ show all passwords
        """
        valid_master = self.confirm_master()
        if valid_master:
            if len(self.passwds) == 1:
                print 'There is no password...'
                return
            for k, v in self.passwds.iteritems():
                if k == 'master':
                    continue
                print ('{k}: {v}').format(k=k, v=v)

        else:
            print 'Wrong password...'

    def create_passwd(self):
        """ create new password
        """
        salt = raw_input('Input a keyword for password (like domain, url) => ')
        while salt is 'master':
            print 'Sorry, you cannot use "master"'
            salt = raw_input('Try it again => ')

        passwd = self.passwd_generator(salt)
        is_updated = self.save_passwd(salt, passwd)
        passwd = passwd if is_updated else self.passwds[salt]
        print 'Password saved int your clipboard.'
        self.setpb_data(passwd)

    def load_passwd(self):
        """ load saved password
        """
        valid_master = self.confirm_master()
        if valid_master:
            salt = raw_input('Input keyword you want to load => ')
            if self.passwds.has_key(salt):
                print 'Password saved int your clipboard.'
                self.setpb_data(self.passwds[salt])
            else:
                print ('Such keyword({0}) is not setted...').format(salt)
        else:
            print 'Wrong password...'

    def update_master(self):
        """ update master password
        """
        valid_master = self.confirm_master()
        if valid_master:
            master = getpass.getpass('Input new master password => ')
            self.passwds['master'] = master
            self._save_db()
            print 'Success!'
        else:
            print 'Wrong password...'

    def delete_passwd(self):
        u"""作成済みのパスワードを削除する
        """
        salt = raw_input('Input keyword you want to delete => ')
        if self.passwds.has_key(salt):
            print ('Deleted {0}.').format(self.passwds[salt])
        else:
            print ('Such keyword({0}) is not setted...').format(salt)
            return
        self.passwds.pop(salt)
        self._save_db()


def main():
    desc = ('{0} [Option] \nDetailed options -h or --help').format(__file__)
    parser = ArgumentParser(description=desc)
    parser.add_argument('-c', '-create', action='store_true', help='Create new password.')
    parser.add_argument('-l', '-load', action='store_true', help="Load saved password by it's keyword.")
    parser.add_argument('-u', '-update', action='store_true', help='Update master password for this tool.')
    parser.add_argument('-d', '-delete', action='store_true', help="Delete a password by it's keyword.")
    parser.add_argument('-list', action='store_true', help='Show all passwords you saved')
    args = parser.parse_args()
    create, load, update, delete, show_list = (
     args.c, args.l, args.u, args.d, args.list)
    if not create and not load and not update and not delete and not show_list:
        parser.error('Please input a option')
    passwordManager = PasswordManager()
    if create:
        passwordManager.create_passwd()
    elif load:
        passwordManager.load_passwd()
    elif update:
        passwordManager.update_master()
    elif delete:
        passwordManager.delete_passwd()
    elif show_list:
        passwordManager.show_passwds()


if __name__ == '__main__':
    main()