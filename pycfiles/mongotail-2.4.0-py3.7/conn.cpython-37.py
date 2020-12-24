# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongotail/conn.py
# Compiled at: 2020-04-09 11:00:48
# Size of source mod 2**32: 3101 bytes
from __future__ import absolute_import
import getpass
from .err import error, error_parsing, ECONNREFUSED
from pymongo import MongoClient
from res_address import get_res_address, AddressError

def connect(address, args):
    """
    Connect with `address`, and return a tuple with a :class:`~pymongo.MongoClient`,
    and a :class:`~pymongo.database.Database` object.
    :param address: a string representation with the db address
    :param args: connection arguments:
    - username: username for authentication (optional)
    - password: password for authentication. If username is given and password isn't,
      it's asked from tty.
    - auth_database: authenticate the username and password against that database (optional).
      If not specified, the database specified in address will be used.
    - ssl, ssl_certfile, ssl_keyfile, ssl_cert_reqs, ssl_ca_certs: SSL authentication options
    :return: a tuple with ``(client, db)``
    """
    try:
        host, port, dbname = get_res_address(address)
    except AddressError as e:
        try:
            error_parsing(str(e).replace('resource', 'database'))
        finally:
            e = None
            del e

    try:
        options = {}
        if args.ssl:
            options['ssl'] = True
            options['ssl_certfile'] = args.ssl_cert_file
            options['ssl_keyfile'] = args.ssl_key_file
            options['ssl_cert_reqs'] = args.ssl_cert_reqs
            options['ssl_ca_certs'] = args.ssl_ca_certs
        client = MongoClient(host=host, port=port, **options)
    except Exception as e:
        try:
            error('Error trying to connect: %s' % str(e), ECONNREFUSED)
        finally:
            e = None
            del e

    username = args.username
    password = args.password
    auth_database = args.auth_database
    if username:
        if password is None:
            password = getpass.getpass()
        else:
            if auth_database is None:
                auth_database = dbname
            try:
                auth_db = client[auth_database]
                auth_db.authenticate(username, password)
            except Exception as e:
                try:
                    error('Error trying to authenticate: %s' % str(e), -3)
                finally:
                    e = None
                    del e

    db = client[dbname]
    return (client, db)