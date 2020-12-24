# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/theme.py
# Compiled at: 2016-03-27 07:48:55
from .context.context import Context
from .compat import text_type
from . import pilot
import json, hashlib, logging
log = logging.getLogger('moya.runtine')
DEFAULT = '\n{\n    "_moya":\n    {\n        "note": "internal default"\n    },\n    "colors":\n    {\n        "text":\n        {\n            "fg": "black",\n            "bg": "white"\n        },\n        "highlight":\n        {\n            "fg": "black",\n            "bg": "wheat"\n        },\n        "selected":\n        {\n            "fg": "white",\n            "bg": "blue"\n        },\n        "border":\n        {\n            "normal": "inherit",\n            "focused": "inherit"\n        }\n    }\n\n}\n'

class Theme(object):
    """Manage theme data."""
    _cache = {}

    @classmethod
    def loader(cls, fs):
        """Automatically add theme to context."""

        def load(context=None):
            if context is None:
                context = pilot.context
            name = context.get('.sys.site.theme', 'default')
            path = ('{}.json').format(name)
            try:
                theme = cls.read(fs, path, context=context)
            except Exception as e:
                log.warning("unable to read theme file '%s' (%s)", path, text_type(e))
                if name != 'default':
                    return load('default')
                log.error("unable to load 'default' theme")
                theme = None

            return theme

        return load

    @classmethod
    def dummy_loader(cls, context):
        """Called when theme is not enabled."""
        log.warning('theme is not set -- add a theme value to your site settings')
        theme_json = DEFAULT
        hasher = hashlib.md5()
        hasher.update(theme_json.encode('utf-8'))
        theme_hash = hasher.hexdigest()
        theme_data = json.loads(theme_json)
        theme_data['_moya'] = {'path': None, 
           'hash': theme_hash}
        return theme_data

    @classmethod
    def read(cls, fs, path, context=None):
        if context is None:
            context = Context()
        hasher = hashlib.md5()
        with fs.open(path, 'rt', encoding='utf-8') as (f):
            theme_json = f.read()
            hasher.update(theme_json.encode('utf-8'))
            theme_hash = hasher.hexdigest()
            theme_data = json.loads(theme_json)
            theme_data['_moya'] = {'path': path, 
               'hash': theme_hash}
        return theme_data