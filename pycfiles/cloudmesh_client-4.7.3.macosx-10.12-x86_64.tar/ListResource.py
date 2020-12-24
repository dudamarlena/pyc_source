# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/ListResource.py
# Compiled at: 2017-04-23 10:30:41
from future.utils import with_metaclass
from cloudmesh_client.common.Printer import Printer

class ListResource(object):

    def _init__(self, category=None, kind=None, order=None, header=None):
        self.category = category
        self.kind = kind

    def info(cls, **kwargs):
        raise NotImplementedError()

    def list(cls, **kwargs):
        raise NotImplementedError()

    def clear(cls, **kwargs):
        raise NotImplementedError()

    def refresh(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, category=None, order=None, output='table'):
        """
        lists the default values in the specified format.
        TODO: This method has a bug as it uses format and output,
        only one should be used.

        :param category: the category of the default value. If general is used
                      it is a special category that is used for global values.
        :param order: The order in which the attributes are returned
        :param output: The output format. json, table, yaml, dict, csv
        :return:
        """
        try:
            if category is None:
                d = cls.cm.all('default')
            else:
                d = cls.cm.find('default', category=category)
            return Printer.dict_printer(d, order=order, output=output)
        except:
            return

        return

    @classmethod
    def set(cls, key, value, category=None, user=None):
        """
        sets the default value for a given category
        :param key: the dictionary key of the value to store it at.
        :param value: the value
        :param category: the name of the category
        :param user: the username to store this default value at.
        :return:
        """
        try:
            o = cls.get_object(key, category)
            me = cls.cm.user or user
            if o is None:
                o = cls.cm.db_obj_dict('default', name=key, value=value, category=category, user=me)
                cls.cm.add_obj(o)
            else:
                o.value = value
                cls.cm.add_from_path(o)
            cls.cm.save()
        except:
            return

        return

    @classmethod
    def get_object(cls, key, category='general'):
        """
        returns the first object that matches the key in the Default
        database.

        :param key: The dictionary key
        :param category: The category
        :return:
        """
        try:
            o = cls.cm.find(category=category, kind='default', output='object', name=key, scope='first')
            return o
        except Exception:
            return

        return

    @classmethod
    def get(cls, key, category='general'):
        """
        returns the value of the first objects matching the key
        with the given category.

        :param key: The dictionary key
        :param category: The category
        :return:
        """
        o = cls.cm.find(category=category, kind='default', output='dict', scope='first', name=key)
        if o is not None:
            return o['value']
        else:
            return
            return

    @classmethod
    def delete(cls, key, category):
        try:
            o = Default.get_object(key, category)
            if o is not None:
                cls.cm.delete(o)
                return 'Deletion. ok.'
            return
        except:
            return

        return

    @classmethod
    def clear(cls):
        """
        deletes all default values in the database.
        :return:
        """
        try:
            d = cls.cm.all('default')
            for item in d:
                name = d[item]['name']
                cls.cm.delete_by_name('default', name)

            cls.cm.save()
        except:
            return

        return