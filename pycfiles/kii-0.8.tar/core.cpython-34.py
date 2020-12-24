# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/hook/core.py
# Compiled at: 2014-12-31 04:01:41
# Size of source mod 2**32: 1338 bytes


class ModelFilters(object):
    __doc__ = 'A registry for storing filters that will be called when model fields\n    are accessed via Model.filtered_<field_name>\n    '
    _hooks = {}

    def register(self, model, field_name, filter_func):
        """Register given filter function on given field name for given model
        """
        model_hooks = self._hooks.setdefault(model, {})
        field_hooks = model_hooks.setdefault(field_name, [])
        if filter_func not in field_hooks:
            field_hooks.append(filter_func)

    def get(self, model, field_name):
        """ return a list of registered filters for given model and field_name
        """
        model_hooks = self._hooks.get(model, None)
        if model_hooks is not None:
            return model_hooks.get(field_name, [])
        return []

    def filter(self, field_name, instance):
        """Return the filtered value of given field on given instance"""
        field = getattr(instance, field_name)
        filtered_value = getattr(field, 'rendered', field)
        for filter_func in self.get(instance.__class__, field_name):
            filtered_value = filter_func(filtered_value, instance=instance)

        return filtered_value

    def clear(self):
        self._hooks.clear()


model_filters = ModelFilters()