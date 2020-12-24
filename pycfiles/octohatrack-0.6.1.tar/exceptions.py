# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmclaughlin/git/LABHR/octohatrack/octohatrack/exceptions.py
# Compiled at: 2015-11-21 05:35:59
import simplejson as json

class ResponseError(Exception):
    """Accessible attributes: error
        error (AttrDict): Parsed error response
    """

    def __init__(self, error):
        Exception.__init__(self, error)
        self.error = error

    def __str__(self):
        return json.dumps(self.error, indent=1)


class OctoHubError(Exception):
    pass