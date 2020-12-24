# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/flask_session_cookie_manager3.py
# Compiled at: 2019-04-25 18:42:35
# Size of source mod 2**32: 5596 bytes
""" Flask Session Cookie Decoder/Encoder """
__author__ = 'Wilson Sumanang, Alexandre ZANNI'
import sys, zlib
from itsdangerous import base64_decode
import ast
if sys.version_info[0] < 3:
    raise Exception('Must be using at least Python 3')
else:
    if sys.version_info[0] == 3:
        if sys.version_info[1] < 4:
            from abc import ABCMeta, abstractmethod
        else:
            from abc import ABC, abstractmethod
    else:
        import argparse
        from flask.sessions import SecureCookieSessionInterface

        class MockApp(object):

            def __init__(self, secret_key):
                self.secret_key = secret_key


        if sys.version_info[0] == 3 and sys.version_info[1] < 4:

            class FSCM(metaclass=ABCMeta):

                def encode(secret_key, session_cookie_structure):
                    """ Encode a Flask session cookie """
                    try:
                        app = MockApp(secret_key)
                        session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
                        si = SecureCookieSessionInterface()
                        s = si.get_signing_serializer(app)
                        return s.dumps(session_cookie_structure)
                    except Exception as e:
                        try:
                            return '[Encoding error] {}'.format(e)
                        finally:
                            e = None
                            del e

                def decode(session_cookie_value, secret_key=None):
                    """ Decode a Flask cookie  """
                    try:
                        if secret_key == None:
                            compressed = False
                            payload = session_cookie_value
                            if payload.startswith('.'):
                                compressed = True
                                payload = payload[1:]
                            data = payload.split('.')[0]
                            data = base64_decode(data)
                            if compressed:
                                data = zlib.decompress(data)
                            return data
                        app = MockApp(secret_key)
                        si = SecureCookieSessionInterface()
                        s = si.get_signing_serializer(app)
                        return s.loads(session_cookie_value)
                    except Exception as e:
                        try:
                            return '[Decoding error] {}'.format(e)
                        finally:
                            e = None
                            del e


        else:

            class FSCM(ABC):

                def encode(secret_key, session_cookie_structure):
                    """ Encode a Flask session cookie """
                    try:
                        app = MockApp(secret_key)
                        session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
                        si = SecureCookieSessionInterface()
                        s = si.get_signing_serializer(app)
                        return s.dumps(session_cookie_structure)
                    except Exception as e:
                        try:
                            return '[Encoding error] {}'.format(e)
                        finally:
                            e = None
                            del e

                def decode(session_cookie_value, secret_key=None):
                    """ Decode a Flask cookie  """
                    try:
                        if secret_key == None:
                            compressed = False
                            payload = session_cookie_value
                            if payload.startswith('.'):
                                compressed = True
                                payload = payload[1:]
                            data = payload.split('.')[0]
                            data = base64_decode(data)
                            if compressed:
                                data = zlib.decompress(data)
                            return data
                        app = MockApp(secret_key)
                        si = SecureCookieSessionInterface()
                        s = si.get_signing_serializer(app)
                        return s.loads(session_cookie_value)
                    except Exception as e:
                        try:
                            return '[Decoding error] {}'.format(e)
                        finally:
                            e = None
                            del e


    if __name__ == '__main__':
        parser = argparse.ArgumentParser(description='Flask Session Cookie Decoder/Encoder',
          epilog='Author : Wilson Sumanang, Alexandre ZANNI')
        subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
        parser_encode = subparsers.add_parser('encode', help='encode')
        parser_encode.add_argument('-s', '--secret-key', metavar='<string>', help='Secret key',
          required=True)
        parser_encode.add_argument('-t', '--cookie-structure', metavar='<string>', help='Session cookie structure',
          required=True)
        parser_decode = subparsers.add_parser('decode', help='decode')
        parser_decode.add_argument('-s', '--secret-key', metavar='<string>', help='Secret key',
          required=False)
        parser_decode.add_argument('-c', '--cookie-value', metavar='<string>', help='Session cookie value',
          required=True)
        args = parser.parse_args()
        if args.subcommand == 'encode':
            if args.secret_key is not None and args.cookie_structure is not None:
                print(FSCM.encode(args.secret_key, args.cookie_structure))
        elif args.subcommand == 'decode':
            if args.secret_key is not None and args.cookie_value is not None:
                print(FSCM.decode(args.cookie_value, args.secret_key))
            else:
                if args.cookie_value is not None:
                    print(FSCM.decode(args.cookie_value))