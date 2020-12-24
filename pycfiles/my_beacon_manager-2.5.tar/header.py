# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rajatg/pyProjects/beacons/beacons/portal/models/header.py
# Compiled at: 2015-12-17 02:20:31


class Header(object):
    """
    OAuth2.0 Header Details
    """

    def get_header_body(self):
        """
        Returns the header of the request
        """
        header = {'Authorization': 'Bearer ' + self.access_token}
        return header

    def __init__(self, access_token):
        self.access_token = access_token

    def __str__(self):
        return self.get_header_body()