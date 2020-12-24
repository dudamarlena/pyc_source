# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/db/s3.py
# Compiled at: 2016-10-28 17:44:13
from .utils import profile_path, load_profile, dump_to_json

class S3(object):
    """
    Simple object for storing AWS credentials
    """

    def __init__(self, access_key, secret_key, profile=None):
        if profile:
            self.load_credentials(profile)
        else:
            self.access_key = access_key
            self.secret_key = secret_key

    def save_credentials(self, profile):
        """
        Saves credentials to a dotfile so you can open them grab them later.

        Parameters
        ----------
        profile: str
            name for your profile (i.e. "dev", "prod")
        """
        filename = profile_path(S3_PROFILE_ID, profile)
        creds = {'access_key': self.access_key, 
           'secret_key': self.secret_key}
        dump_to_json(filename, creds)

    def load_credentials(self, profile):
        """
        Loads crentials for a given profile. Profiles are stored in
        ~/.db.py_s3_{profile_name} and are a base64 encoded JSON file. This is
        not to say this a secure way to store sensitive data, but it will
        probably stop your little sister from spinning up EC2 instances.

        Parameters
        ----------
        profile: str
            identifier/name for your database (i.e. "dev", "prod")
        """
        f = profile_path(S3_PROFILE_ID, profile)
        if os.path.exists(f):
            creds = load_profile(f)
            if 'access_key' not in creds:
                raise Exception(("`access_key` not found in s3 profile '{0}'").format(profile))
            self.access_key = creds['access_key']
            if 'access_key' not in creds:
                raise Exception(("`secret_key` not found in s3 profile '{0}'").format(profile))
            self.secret_key = creds['secret_key']