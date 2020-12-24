# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aneumeier/web/env/lib/python2.7/site-packages/flattr/__init__.py
# Compiled at: 2013-06-20 11:16:16
"""
__init__.py 

"""
import json, oauth2 as oauth, time
version_info = (0, 0, 16)
__version__ = ('.').join(map(str, version_info))
FLATTR_API = 'https://api.flattr.com'
FLATTR_API_ENDPOINT = 'https://api.flattr.com/rest/v2'
FLATTR_OAUTH2_AUTHORIZE = 'https://flattr.com/oauth/authorize'
FLATTR_OAUTH2_TOKEN = 'https://flattr.com/oauth/token'

class FlattrError(Exception):
    """
    Base class for Flattr errors
    """

    @property
    def message(self):
        """
        Returns the first argument used to construct this error.
        """
        return self.args[0]


class Ouath2API(object):
    token = None
    params = {'oauth_version': '2.0', 
       'oauth_nonce': oauth.generate_nonce(), 
       'oauth_timestamp': int(time.time())}

    def __init__(self, token):
        self.token = token

    def get(self, url, params=None):
        if not params:
            params = self.params
        req = oauth.Request(method='GET', url=url, parameters=params)
        return json.dumps(req)


class Flattr(object):
    """
    The flattr object.
    See:: http://developers.flattr.net/api/resources/flattrs/

    Field       Type      Permission  Description
    type        string                Object type, set to flattr.
    thing       hash                  Contains a thing object.
    owner       hash                  Contains either a user object or a mini user object (default).
    created_at  string                Format is unixtime.
    """

    def __init__(self):
        pass


class Thing(object):
    """
    The Thing object.
    See:: http://developers.flattr.net/api/resources/things/

    Field               Type      Permission      Description
    type                string                    Object type, set to thing.
    resource            string                    URL to the API resource
    link                string                    URL to user on Flattr.com website
    id                  int                       ID of the thing
    url                 string                    URL the thing is pointing to
    flattrs             int                       Number of flattrs
    flattrs_user_count  int                       Number of user who have flattred
    title               string                    Title of the thing
    description         string                    Description of the thing
    tags                array                     Array with tags as strings
    language            string                    Langauge
    category            string                    Category
    created_at          int                       Format is unixtime
    owner               hash                      Contains either a user object or a mini user object (default).
    hidden              bool                      Hidden or not in listings. Example, API search and Catalog.
    image               string                    URL to thing image
    flattred            bool      authenticated   Has the authenticated user flattred the thing
    last_flattr_at      int       owner           Last time flattred. Format is unixtime. Only available if the authenticated user owns the thing.
    updated_at          int       owner           Last time updated. Format is unixtime. Only available if the authenticated user owns the thing.
    """

    def __init__(self, *args, **kwargs):
        pass


class Subscription(object):
    """
    The Subscription object.
    See:: http://developers.flattr.net/api/resources/subscriptions/
    """

    def __init__(self, *args, **kwargs):
        pass


class FlattrUser(object):
    """
    The User object.
    See:: http://developers.flattr.net/api/resources/users/

    type                string                          Object type, set to user.
    resource            string                          URL to the API resource
    link                    string                              URL to user on Flattr.com website
    username            string                          Username on Flattr
    url                 string                          URL set by the user
    firstname           string          
    lastname            string          
    avatar                  string                              URL to a Flattr avatar, size: 48x48px
    about                   string                              Short description about the user
    city                    string              
    country                 string              
    email                   string      email, extendedread     
    registered_at           int     extendedread            Format is unixtime
    """

    def __init__(self, *args, **kwargs):
        pass


class FlattrMiniUser(object):
    """
    The MiniUser object.
    See:: http://developers.flattr.net/api/resources/users/
    
    type                string                          Object type, set to user.
    resource            string                          URL to the API resource
    link                    string                              URL to user on Flattr.com website
    username            string                          Username on Flattr
    """

    def __init__(self, *args, **kwargs):
        pass


class Activities(object):
    """
    The Activities object.
    See:: http://developers.flattr.net/api/resources/activities/
    """

    def __init__(self, *args, **kwargs):
        pass


class Categories(Ouath2API):
    """
    The Categories object.
    See:: http://developers.flattr.net/api/resources/categories/
    """

    def __init__(self, *args, **kwargs):
        pass

    def list(self):
        url = '%s/rest/v2/categories' % FLATTR_API
        return self.get(url)