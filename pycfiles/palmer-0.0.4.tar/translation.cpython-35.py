# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/loup/Workspace/Projects/personal/palmer/palmer/utils/translation.py
# Compiled at: 2016-11-16 03:37:50
# Size of source mod 2**32: 278 bytes
from flask import current_app
from speaklater import make_lazy_gettext
from palmer.config import default_config
config = current_app.api_config if current_app else default_config
lazy_gettext = make_lazy_gettext(lambda : getattr(config, 'GETTEXT_FUNC'))