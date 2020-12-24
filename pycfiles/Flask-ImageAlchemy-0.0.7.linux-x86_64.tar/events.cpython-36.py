# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ppoteralski/PycharmProjects/sqlalchemy-stdimage/.venv/lib/python3.6/site-packages/flask_image_alchemy/events.py
# Compiled at: 2017-03-10 03:24:21
# Size of source mod 2**32: 790 bytes
from flask_image_alchemy.fields import StdImageFile
from sqlalchemy import inspect
from werkzeug.datastructures import FileStorage

def before_delete_delete_callback(mapper, connection, instance):
    for field in mapper.attrs:
        instance_field = getattr(instance, field.key)
        if isinstance(instance_field, StdImageFile):
            instance_field.delete(variations=True)


def before_update_delete_callback(mapper, connection, instance):
    state = inspect(instance)
    for field in mapper.attrs:
        instance_field = getattr(instance, field.key)
        if isinstance(instance_field, FileStorage):
            hist = state.get_history(field.key, True)
            if hist.deleted:
                for i in hist.deleted:
                    i.delete(variations=True)