# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/filter.py
# Compiled at: 2019-03-19 08:10:19
# Size of source mod 2**32: 4230 bytes


class Filter:
    pass


class LastSession(Filter):
    __doc__ = 'Filtered by the last session of the user\n\n    Arguments:\n        relation: "<" or ">"\n        hours_ago: number of hours before or after the users last session\n    '

    def __init__(self, relation, hours_ago):
        self.data = {'field':'last_session', 
         'relation':relation, 
         'hours_ago':hours_ago}


class FirstSession(Filter):
    __doc__ = 'Filtered by the first session of the user\n\n    Arguments:\n        relation: "<" or ">"\n        hours_ago: number of hours before or after the users last session\n    '

    def __init__(self, relation, hours_ago):
        self.data = {'field':'first_session', 
         'relation':relation, 
         'hours_ago':hours_ago}


class SessionCount(Filter):
    __doc__ = 'Filtered by amount of sessions\n\n    Arguments:\n        relation: "<", ">", "=" or "!="\n        value: time in seconds the user has been in your app\n    '

    def __init__(self, relation, value):
        self.data = {'field':'session_count', 
         'value':value}


class SessionTime(Filter):
    __doc__ = 'Filtered by time the user has been in app\n\n    Arguments:\n        relation: "<" or ">"\n        value: time in seconds the user has been in your app\n    '

    def __init__(self, relation, value):
        self.data = {'field':'session_time', 
         'value':value}


class AmountSpent(Filter):
    __doc__ = 'Filtered by amount spent on IAP\n\n    Arguments:\n        relation: "<", ">" or "="\n        value: amount in USD a user has spent on IAP (In App Purchases)\n    '

    def __init__(self, relation, value):
        self.data = {'field':'amount_spent', 
         'value':value}


class BoughtSku(Filter):
    __doc__ = 'Filtered by SKU purchased\n\n    Arguments:\n        relation: "<",  ">" or "="\n        key: SKU purchased in your app as an IAP (In App Purchases)\n        value: value of SKU to compare to\n    '

    def __init__(self, relation, key, value):
        self.data = {'field':'bought_sku', 
         'relation':relation, 
         'key':key, 
         'value':value}


class Tag(Filter):
    __doc__ = 'Filtered by tag\n\n    Arguments:\n        relation: "<", ">", "=", "!=", "exists" or "not_exists"\n        key: tag to compare\n        value: time in seconds the user has been in your app\n    '

    def __init__(self, key, relation, value):
        self.data = {'field':'tag', 
         'key':key, 
         'relation':relation, 
         'value':value}


class Language(Filter):
    __doc__ = 'Filtered by language of user\n\n    Arguments:\n        relation: "=" or "!="\n        value: 2 character language code\n    '

    def __init__(self, relation, value):
        self.data = {'field':'language', 
         'relation':relation, 
         'value':value}


class AppVersion(Filter):
    __doc__ = 'Filtered by version of the app\n\n    Arguments:\n        relation: "<", ">", "=" or "!="\n        value: app version\n    '

    def __init__(self, relation, value):
        self.data = {'field':'app_version', 
         'relation':relation, 
         'value':value}


class Location(Filter):
    __doc__ = 'Filtered by location of the user\n\n    Arguments:\n        radius: in meters\n        lat: latitude\n        long: longitude\n    '

    def __init__(self, radius, lat, long):
        self.data = {'field':'location', 
         'radius':radius, 
         'lat':lat, 
         'long':long}


class Email(Filter):
    __doc__ = 'Filtered by time the user has been in app\n\n    For email targeting only, not used to send push notifications\n\n    Arguments:\n        value: email address\n    '

    def __init__(self, value):
        self.data = {'field':'email', 
         'value':value}


class Country(Filter):
    __doc__ = 'Filtered by country of the user\n\n    Arguments:\n        relation: "="\n        value: 2 character country code\n    '

    def __init__(self, value):
        self.data = {'field':'country', 
         'value':value}