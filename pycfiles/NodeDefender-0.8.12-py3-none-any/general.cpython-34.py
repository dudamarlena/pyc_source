# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/setup/general.py
# Compiled at: 2018-03-08 08:42:37
# Size of source mod 2**32: 1636 bytes
from NodeDefender.manage.setup import manager, print_message, print_topic, print_info
from flask_script import prompt
import NodeDefender

@manager.command
def general():
    port = None
    while port is None:
        port = prompt('Which port should the server be running on')

    print_info('Security Key is used to Encrypt Password etc.')
    key = None
    while key is None:
        key = prompt('Enter Secret Key')

    print_info('Salt is used to genereate URLS and more.')
    salt = None
    while salt is None:
        salt = prompt('Please enter Salt')

    print_info('You can either have users register by themselfs on the               authentication- page or via invite mail. Invite mail requires               that you also enable mail- support so that NodeDefender can send               invitation- mail and such. Superuser can still administrate               users in the same way.')
    self_registration = None
    while self_registration is None:
        self_registration = prompt('Enable self-registration(Y/N)').upper()
        if 'Y' in self_registration:
            self_registration = True
        elif 'N' in self_registration:
            self_registration = False
        else:
            self_registration = None

    NodeDefender.config.general.set(port=port, key=key, salt=salt, self_registration=self_registration)
    if NodeDefender.config.general.write():
        print_info('General- config successfully written')
    return True