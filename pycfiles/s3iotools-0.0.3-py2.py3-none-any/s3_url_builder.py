# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: s3iotools/utils/s3_url_builder.py
# Compiled at: 2019-05-20 08:45:08
"""
There are two simple rules for s3 object key:

- should not start with slash "/"
- should not end with slash "/"

sometime we made mistake on this, this helper function ensure that common mistake
will not happened in building s3 URI.
"""

class S3UrlBuilder(object):
    """
    Build AWS S3 relative url.
    """
    URL_TPL = 'https://s3.amazonaws.com/{bucket_name}/{key}'
    S3_URI_TPL = 's3://{bucket_name}/{key}'

    def ensure_not_startswith_slash(self, key):
        """
        S3 Key has to obey these rules:

        - cannot startswith ``/``.
        - if it is an directory object, it has to endswith ``/``.
        - if it is an file object, it can't endswith ``/``.
        """
        if key.startswith('/'):
            key = key[1:]
        return key

    def build_url_by_key(self, bucket_name, key):
        """
        Build the url to access the s3 object from browser.

        :param bucket_name: str, bucket name.
        :param key: str, posix styled path.
        :return: str.
        """
        key = self.ensure_not_startswith_slash(key)
        return self.URL_TPL.format(bucket_name=bucket_name, key=key)

    def build_s3_uri_by_key(self, bucket_name, key):
        """
        Build the universal resource identifier consumed by ``pandas.read_csv``.

        :param bucket_name: str, bucket name.
        :param key: str, posix styled path.
        :return: str.
        """
        key = self.ensure_not_startswith_slash(key)
        return self.S3_URI_TPL.format(bucket_name=bucket_name, key=key)

    def build_key_by_parts(self, *parts):
        l = list()
        for part in parts:
            for i in part.split('/'):
                if i.strip():
                    l.append(i)

        return ('/').join(l)


s3_url_builder = S3UrlBuilder()