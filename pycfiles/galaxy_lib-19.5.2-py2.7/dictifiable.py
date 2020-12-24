# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/dictifiable.py
# Compiled at: 2018-04-20 03:19:42
import datetime, uuid

class Dictifiable(object):
    """ Mixin that enables objects to be converted to dictionaries. This is useful
        when for sharing objects across boundaries, such as the API, tool scripts,
        and JavaScript code. """

    def to_dict(self, view='collection', value_mapper=None):
        """
        Return item dictionary.
        """
        if not value_mapper:
            value_mapper = {}

        def get_value(key, item):
            """
            Recursive helper function to get item values.
            """
            try:
                return item.to_dict(view=view, value_mapper=value_mapper)
            except Exception:
                if key in value_mapper:
                    return value_mapper.get(key)(item)
                if type(item) == datetime.datetime:
                    return item.isoformat()
                if type(item) == uuid.UUID:
                    return str(item)
                return item

        rval = dict(model_class=self.__class__.__name__)
        try:
            visible_keys = self.__getattribute__('dict_' + view + '_visible_keys')
        except AttributeError:
            raise Exception('Unknown Dictifiable view: %s' % view)

        for key in visible_keys:
            try:
                item = self.__getattribute__(key)
                if isinstance(item, list):
                    rval[key] = []
                    for i in item:
                        rval[key].append(get_value(key, i))

                else:
                    rval[key] = get_value(key, item)
            except AttributeError:
                rval[key] = None

        return rval