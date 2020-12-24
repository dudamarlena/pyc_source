# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ricardobanffy/projects/appengine-fixture-loader/.env/lib/python2.7/site-packages/appengine_fixture_loader/loader.py
# Compiled at: 2016-07-21 08:19:20
__doc__ = '\nTools to automate loading of test fixtures\n'
import json
from datetime import datetime, time, date
from google.appengine.ext.ndb.model import DateTimeProperty, DateProperty, TimeProperty

def _sensible_value(attribute_type, value):
    if type(attribute_type) is DateTimeProperty:
        retval = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    elif type(attribute_type) is TimeProperty:
        try:
            dt = datetime.strptime(value, '%H:%M:%S')
        except ValueError:
            dt = datetime.strptime(value, '%H:%M')

        retval = time(dt.hour, dt.minute, dt.second)
    elif type(attribute_type) is DateProperty:
        dt = datetime.strptime(value, '%Y-%m-%d')
        retval = date(dt.year, dt.month, dt.day)
    else:
        retval = value
    return retval


def load_fixture(filename, kind, post_processor=None):
    """
    Loads a file into entities of a given class, run the post_processor on each
    instance before it's saved
    """

    def _load(od, kind, post_processor, parent=None, presets={}):
        """
        Loads a single dictionary (od) into an object, overlays the values in
        presets, persists it and
        calls itself on the objects in __children__* keys
        """
        if hasattr(kind, 'keys'):
            objtype = kind[od['__kind__']]
        else:
            objtype = kind
        obj_id = od.get('__id__')
        if obj_id is not None:
            obj = objtype(id=obj_id, parent=parent)
        else:
            obj = objtype(parent=parent)
        for attribute_name in [ k for k in od.keys() if not k.startswith('__') and not k.endswith('__')
                              ] + presets.keys():
            attribute_type = objtype.__dict__[attribute_name]
            attribute_value = _sensible_value(attribute_type, presets.get(attribute_name, od.get(attribute_name)))
            obj.__dict__['_values'][attribute_name] = attribute_value

        if post_processor:
            post_processor(obj)
        obj.put()
        loaded = [
         obj]
        for item in od.get('__children__', []):
            loaded.extend(_load(item, kind, post_processor, parent=obj.key))

        for child_attribute_name in [ k for k in od.keys() if k.startswith('__children__') and k != '__children__'
                                    ]:
            attribute_name = child_attribute_name.split('__')[(-2)]
            for child in od[child_attribute_name]:
                loaded.extend(_load(child, kind, post_processor, presets={attribute_name: obj.key}))

        return loaded

    tree = json.load(open(filename))
    loaded = []
    for item in tree:
        loaded.extend(_load(item, kind, post_processor))

    return loaded