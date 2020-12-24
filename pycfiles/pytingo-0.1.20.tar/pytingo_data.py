# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/castarco/Proyectos/Pytingo/pytingo/pytingo_data.py
# Compiled at: 2014-06-19 10:48:54
from __future__ import absolute_import, division, print_function, unicode_literals
import copy, six

class PytingoData:
    """
    """

    def __init__(self, data_dict, process_meta=True, meta_field=b'.meta', separator=b'.', wildcard=b'*', list_accessor=b'$'):
        """
        Args:
            :param data_dict:
            :type data_dict:

            :param process_meta:
            :type process_meta:

            :param meta_field:
            :type meta_field:

            :param separator:
            :type separator:

            :param wildcard:
            :type wildcard:
        """
        if not isinstance(data_dict, dict):
            raise ValueError(b'data_dict must be of type dict.')
        if not isinstance(process_meta, bool):
            raise ValueError(b'process_meta must be of type bool.')
        if not isinstance(meta_field, six.string_types):
            raise ValueError(b'meta_field must be of type str.')
        if not isinstance(separator, six.string_types):
            raise ValueError(b'separator must be of type str.')
        if not isinstance(wildcard, six.string_types):
            raise ValueError(b'wildcard must be of type str.')
        if not isinstance(list_accessor, six.string_types):
            raise ValueError(b'list_accessor must be of type str.')
        self._data_dict = copy.deepcopy(data_dict)
        self._meta_field = meta_field
        self._separator = separator
        self._wildcard = wildcard
        self._list_accessor = list_accessor
        if not process_meta or self._meta_field not in self._data_dict:
            self._meta = {}
            self._processed_data_dict = self._data_dict
        else:
            self._meta = self._data_dict.pop(self._meta_field)
            self._process_meta()

    def _process_meta(self):
        """
        """
        self._processed_data_dict = copy.deepcopy(self._data_dict)
        if b'inheritance' in self._meta:
            self._process_inheritance()

    def _process_inheritance(self):
        """
        """
        inheritance = self._meta[b'inheritance']
        for inheritor_str_path in inheritance:
            inheritors = self._get_inheritors(inheritor_str_path.split(self._separator))
            for inheritor in inheritors:
                if isinstance(inheritor, dict):
                    for inheritable_value_key in inheritance[inheritor_str_path]:
                        if inheritable_value_key in inheritor:
                            continue
                        try:
                            inheritor[inheritable_value_key] = self.get(inheritable_value_key)
                        except KeyError:
                            pass

                elif isinstance(inheritor, list):
                    pass
                else:
                    raise ValueError(b"A field pointed by the path '" + inheritor_str_path + b"' is an atomic value and can't inherit anything.")

    def _get_inheritors(self, path, tracepoint=None):
        if tracepoint is None:
            if path == []:
                raise RuntimeError(b'There is no point to make . inheriting from a subfield.')
            tracepoint = self._processed_data_dict
        key = path[0]
        if isinstance(tracepoint, dict):
            if key == self._wildcard:
                inheritors = []
                selected_items_type = None
                for tp_key in tracepoint:
                    item_type = type(tracepoint[tp_key])
                    if selected_items_type is None:
                        selected_items_type = item_type
                    elif selected_items_type != item_type:
                        raise ValueError(b'The items types must be uniform when the items are selected with a wildcard.')
                    if len(path) == 1:
                        inheritors.append(tracepoint[tp_key])
                    else:
                        inheritors.extend(self._get_inheritors(path[1:], tracepoint[tp_key]))

                return inheritors
            if key in tracepoint:
                if len(path) == 1:
                    return [tracepoint[key]]
                return self._get_inheritors(path[1:], tracepoint[key])
            return []
        else:
            if isinstance(tracepoint, list):
                inheritors = []
                selected_items_type = None
                for item in tracepoint:
                    item_type = type(item)
                    if selected_items_type is None:
                        selected_items_type = item_type
                    elif selected_items_type != item_type:
                        raise ValueError(b'The items types must be uniform when the items are selected with a wildcard.')
                    inheritors.extend(self._get_inheritors(path if key != self._wildcard else path[1:], item))

                return inheritors
            return []
        return

    def as_dict(self):
        return copy.deepcopy(self._processed_data_dict)

    def get(self, key):
        """
        This method gives us a value of our SettingsData object.
        If the given key refers to an intermediate subdictionary, then
        a new SettingsData object is returned.
        """
        value = self._processed_data_dict
        for _key in key.split(self._separator):
            if _key != b'':
                if isinstance(value, dict):
                    value = value[_key]
                elif isinstance(value, list):
                    value = value[int(_key)]

        if isinstance(value, dict):
            return PytingoData(value, False, self._meta_field, self._separator, self._wildcard, self._list_accessor)
        else:
            return value

    def __getattr__(self, attr):
        """
        Convenient accessor.
        """
        return self.get(attr)

    def __eq__(self, b):
        for k in self._processed_data_dict:
            if self.get(k) != b.get(k):
                return False

        return True

    def __ne__(self, b):
        return not self.__eq__(b)

    def __contains__(self, item):
        try:
            self.get(item)
            return True
        except KeyError:
            return False