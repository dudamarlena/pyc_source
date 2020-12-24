# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/users.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 4782 bytes
from __future__ import print_function
import sys, six
from mediagoblin.db.models import LocalUser
from mediagoblin.gmg_commands import util as commands_util
from mediagoblin import auth
from mediagoblin import mg_globals

def adduser_parser_setup(subparser):
    subparser.add_argument('--username', '-u', help='Username used to login')
    subparser.add_argument('--password', '-p', help='Your supersecret word to login, beware of storing it in bash history')
    subparser.add_argument('--email', '-e', help='Email to receive notifications')


def adduser(args):
    commands_util.setup_app(args)
    args.username = six.text_type(commands_util.prompt_if_not_set(args.username, 'Username:'))
    args.password = commands_util.prompt_if_not_set(args.password, 'Password:', True)
    args.email = commands_util.prompt_if_not_set(args.email, 'Email:')
    db = mg_globals.database
    users_with_username = db.LocalUser.query.filter(LocalUser.username == args.username.lower()).count()
    if users_with_username:
        print('Sorry, a user with that name already exists.')
        sys.exit(1)
    else:
        entry = db.LocalUser()
        entry.username = six.text_type(args.username.lower())
        entry.email = six.text_type(args.email)
        entry.pw_hash = auth.gen_password_hash(args.password)
        default_privileges = [
         db.Privilege.query.filter(db.Privilege.privilege_name == 'commenter').one(),
         db.Privilege.query.filter(db.Privilege.privilege_name == 'uploader').one(),
         db.Privilege.query.filter(db.Privilege.privilege_name == 'reporter').one(),
         db.Privilege.query.filter(db.Privilege.privilege_name == 'active').one()]
        entry.all_privileges = default_privileges
        entry.save()
        print('User created (and email marked as verified).')


def makeadmin_parser_setup(subparser):
    subparser.add_argument('username', help='Username to give admin level', type=six.text_type)


def makeadmin(args):
    commands_util.setup_app(args)
    db = mg_globals.database
    user = db.LocalUser.query.filter(LocalUser.username == args.username.lower()).first()
    if user:
        user.all_privileges.append(db.Privilege.query.filter(db.Privilege.privilege_name == 'admin').one())
        user.save()
        print('The user %s is now an admin.' % args.username)
    else:
        print("The user %s doesn't exist." % args.username)
        sys.exit(1)


def changepw_parser_setup(subparser):
    subparser.add_argument('username', help='Username used to login', type=six.text_type)
    subparser.add_argument('password', help='Your NEW supersecret word to login')


def changepw(args):
    commands_util.setup_app(args)
    db = mg_globals.database
    user = db.LocalUser.query.filter(LocalUser.username == args.username.lower()).first()
    if user:
        user.pw_hash = auth.gen_password_hash(args.password)
        user.save()
        print('Password successfully changed for user %s.' % args.username)
    else:
        print("The user %s doesn't exist." % args.username)
        sys.exit(1)


def deleteuser_parser_setup(subparser):
    subparser.add_argument('username', help='Username to delete', type=six.text_type)


def deleteuser(args):
    commands_util.setup_app(args)
    db = mg_globals.database
    user = db.LocalUser.query.filter(LocalUser.username == args.username.lower()).first()
    if user:
        user.delete()
        print('The user %s has been deleted.' % args.username)
    else:
        print("The user %s doesn't exist." % args.username)
        sys.exit(1)