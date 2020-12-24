# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sts/credentials.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8210 bytes
import os, datetime, boto.utils
from boto.compat import json

class Credentials(object):
    __doc__ = '\n    :ivar access_key: The AccessKeyID.\n    :ivar secret_key: The SecretAccessKey.\n    :ivar session_token: The session token that must be passed with\n                         requests to use the temporary credentials\n    :ivar expiration: The timestamp for when the credentials will expire\n    '

    def __init__(self, parent=None):
        self.parent = parent
        self.access_key = None
        self.secret_key = None
        self.session_token = None
        self.expiration = None
        self.request_id = None

    @classmethod
    def from_json(cls, json_doc):
        """
        Create and return a new Session Token based on the contents
        of a JSON document.

        :type json_doc: str
        :param json_doc: A string containing a JSON document with a
            previously saved Credentials object.
        """
        d = json.loads(json_doc)
        token = cls()
        token.__dict__.update(d)
        return token

    @classmethod
    def load(cls, file_path):
        """
        Create and return a new Session Token based on the contents
        of a previously saved JSON-format file.

        :type file_path: str
        :param file_path: The fully qualified path to the JSON-format
            file containing the previously saved Session Token information.
        """
        fp = open(file_path)
        json_doc = fp.read()
        fp.close()
        return cls.from_json(json_doc)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'AccessKeyId':
            self.access_key = value
        else:
            if name == 'SecretAccessKey':
                self.secret_key = value
            else:
                if name == 'SessionToken':
                    self.session_token = value
                else:
                    if name == 'Expiration':
                        self.expiration = value
                    elif name == 'RequestId':
                        self.request_id = value

    def to_dict(self):
        """
        Return a Python dict containing the important information
        about this Session Token.
        """
        return {'access_key': self.access_key,  'secret_key': self.secret_key, 
         'session_token': self.session_token, 
         'expiration': self.expiration, 
         'request_id': self.request_id}

    def save(self, file_path):
        """
        Persist a Session Token to a file in JSON format.

        :type path: str
        :param path: The fully qualified path to the file where the
            the Session Token data should be written.  Any previous
            data in the file will be overwritten.  To help protect
            the credentials contained in the file, the permissions
            of the file will be set to readable/writable by owner only.
        """
        fp = open(file_path, 'w')
        json.dump(self.to_dict(), fp)
        fp.close()
        os.chmod(file_path, 384)

    def is_expired(self, time_offset_seconds=0):
        """
        Checks to see if the Session Token is expired or not.  By default
        it will check to see if the Session Token is expired as of the
        moment the method is called.  However, you can supply an
        optional parameter which is the number of seconds of offset
        into the future for the check.  For example, if you supply
        a value of 5, this method will return a True if the Session
        Token will be expired 5 seconds from this moment.

        :type time_offset_seconds: int
        :param time_offset_seconds: The number of seconds into the future
            to test the Session Token for expiration.
        """
        now = datetime.datetime.utcnow()
        if time_offset_seconds:
            now = now + datetime.timedelta(seconds=time_offset_seconds)
        ts = boto.utils.parse_ts(self.expiration)
        delta = ts - now
        return delta.total_seconds() <= 0


class FederationToken(object):
    __doc__ = '\n    :ivar credentials: A Credentials object containing the credentials.\n    :ivar federated_user_arn: ARN specifying federated user using credentials.\n    :ivar federated_user_id: The ID of the federated user using credentials.\n    :ivar packed_policy_size: A percentage value indicating the size of\n                             the policy in packed form\n    '

    def __init__(self, parent=None):
        self.parent = parent
        self.credentials = None
        self.federated_user_arn = None
        self.federated_user_id = None
        self.packed_policy_size = None
        self.request_id = None

    def startElement(self, name, attrs, connection):
        if name == 'Credentials':
            self.credentials = Credentials()
            return self.credentials
        else:
            return

    def endElement(self, name, value, connection):
        if name == 'Arn':
            self.federated_user_arn = value
        else:
            if name == 'FederatedUserId':
                self.federated_user_id = value
            else:
                if name == 'PackedPolicySize':
                    self.packed_policy_size = int(value)
                elif name == 'RequestId':
                    self.request_id = value


class AssumedRole(object):
    __doc__ = '\n    :ivar user: The assumed role user.\n    :ivar credentials: A Credentials object containing the credentials.\n    '

    def __init__(self, connection=None, credentials=None, user=None):
        self._connection = connection
        self.credentials = credentials
        self.user = user

    def startElement(self, name, attrs, connection):
        if name == 'Credentials':
            self.credentials = Credentials()
            return self.credentials
        if name == 'AssumedRoleUser':
            self.user = User()
            return self.user

    def endElement(self, name, value, connection):
        pass


class User(object):
    __doc__ = '\n    :ivar arn: The arn of the user assuming the role.\n    :ivar assume_role_id: The identifier of the assumed role.\n    '

    def __init__(self, arn=None, assume_role_id=None):
        self.arn = arn
        self.assume_role_id = assume_role_id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Arn':
            self.arn = value
        elif name == 'AssumedRoleId':
            self.assume_role_id = value


class DecodeAuthorizationMessage(object):
    __doc__ = '\n    :ivar request_id: The request ID.\n    :ivar decoded_message: The decoded authorization message (may be JSON).\n    '

    def __init__(self, request_id=None, decoded_message=None):
        self.request_id = request_id
        self.decoded_message = decoded_message

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'requestId':
            self.request_id = value
        elif name == 'DecodedMessage':
            self.decoded_message = value