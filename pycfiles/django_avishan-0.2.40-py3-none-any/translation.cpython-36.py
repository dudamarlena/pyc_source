# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/misc/translation.py
# Compiled at: 2020-05-09 06:04:11
# Size of source mod 2**32: 1148 bytes
from avishan.configure import get_avishan_config

class AvishanTranslatable:
    EN = None
    FA = None

    def __init__(self, **kwargs):
        """
        translatable texts
        :param kwargs: keys like: FA, EN
        """
        for key, value in kwargs.items():
            self.__setattr__(key.upper(), value)

    def __str__(self):
        from avishan import current_request
        from avishan.exceptions import ErrorMessageException
        if 'language' not in current_request.keys():
            try:
                return list(self.__dict__.values())[0]
            except IndexError:
                return 'Not translated string'

        try:
            if current_request['language'] is None:
                lang = get_avishan_config().LANGUAGE
            else:
                lang = current_request['language']
            if self.__dict__[lang.upper()] is not None:
                return self.__dict__[lang.upper()]
            raise ValueError
        except:
            raise ErrorMessageException('Not translated string')