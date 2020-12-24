# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/orm/drivers/mongo/model.py
# Compiled at: 2013-03-09 13:14:07
from bson import ObjectId
from frame.orm.errors import ValidateError, RequiredFieldError, ExtraFieldError, ModelLoadError
from frame.orm.datatypes import CustomType
from frame.forms import BasicForm
from frame.treedict import TreeDict

class Model(object):
    structure = {}
    required_fields = []
    default_values = {}
    unique_fields = []
    hidden_fields = []

    def __init__(self, data={}, **kwargs):
        data = dict(data)
        if '_id' not in data and '_id' not in kwargs:
            data['_id'] = ObjectId()
        defaults = dict(self.default_values)
        self._setup_defaults(defaults)
        self._data = {}
        self._tree_data = TreeDict(self._data)
        self._tree_data.update_tree(defaults)
        self._tree_data.update_tree(data)
        self._tree_data.update_tree(dict(kwargs))
        self.make_form = self.make_edit_form

    def __getstate__(self):
        copied_dict = self.__dict__.copy()
        if 'make_form' in copied_dict:
            del copied_dict['make_form']
        return copied_dict

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        else:
            if key in self.structure:
                return
            raise KeyError('Could not access item %s' % key)
            return

    def __setitem__(self, key, value):
        if key in self.structure:
            self._data[key] = value
        else:
            raise KeyError("Cannot save the key '%s' as it is not defind as part of this data structure." % key)

    def __delitem__(self, key):
        del self._data[key]

    def __getattr__(self, key):
        if key == '__setstate__':
            return object.__getattr__(self, key)
        else:
            if key in self._data:
                return self._data[key]
            if key in self.structure:
                return
            raise AttributeError
            return

    def __delattr__(self, key):
        try:
            del self._data[key]
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        if key in ('_data', 'make_form', '_tree_data') or key.endswith('__'):
            object.__setattr__(self, key, value)
        elif key in self.structure:
            self._data[key] = value
        else:
            raise AttributeError('Cannot set attribute %s' % key)

    def __contains__(self, key):
        return key in self._data

    def __repr__(self):
        data = dict(self.structure)
        data.update(self._data)
        return str(data)

    @classmethod
    def make_new_form(self, action, data={}, failed_items=[], *args, **kwargs):
        return BasicForm(self, data).render(action=action, new=True, failed_items=failed_items, *args, **kwargs)

    def make_edit_form(self, action, failed_items=[], *args, **kwargs):
        return BasicForm(self, self._data).render(action=action, new=False, failed_items=failed_items, *args, **kwargs)

    make_form = make_new_form

    def items(self):
        return self._data.items()

    def update(self, data, tree=True):
        if tree:
            self._tree_data.update_tree(data)
        else:
            self._tree_data.update(data)

    def _setup_defaults(self, data):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict) or hasattr(v, '__iter__'):
                    self._setup_defaults(v)
                elif hasattr(v, '__call__'):
                    data[k] = v()

        elif hasattr(data, '__iter__'):
            for i in xrange(len(data)):
                if hasattr(data[i], '__call__'):
                    data[i] = data[i]()

    @property
    def collection(self):
        return self.get_collection()

    @classmethod
    def get_collection(self):
        return self.__connection__[self.__database__][self.__collection__]

    def save(self, safe=True, *args, **kwargs):
        self.validate()
        if safe:
            return self.get_collection().save(self._data, safe=True, *args, **kwargs)
        else:
            return self.get_collection().save(self._data, *args, **kwargs)

    def remove(self):
        self.collection.remove({'_id': self._id})

    def _check_required_fields(self):
        missing_fields = [ i for i in self.required_fields if i not in self._tree_data ]
        if missing_fields:
            raise RequiredFieldError('Required field(s) missing: %s' % (', ').join(missing_fields))

    def _check_data_types(self, data, structure):
        """
                Checks to see if everything is all right with data types and what not. Also returns
                a list of fields that don't belong, if any.
                """
        extra_fields = []
        structure = TreeDict(structure)
        for k, v in data.items():
            if k not in ('_id', ):
                if k in structure:
                    data[k] = structure[k](v)
                elif k not in structure:
                    extra_fields.append(k)
                    del data[k]

        return extra_fields

    def prep_data(self, data):
        pass

    def validate(self):
        self._check_required_fields()
        extra_fields = self._check_data_types(self._tree_data, self.structure)
        self.prep_data(self._data)

    @classmethod
    def find(self, *args, **kwargs):
        result = self.get_collection().find(*args, **kwargs)
        for i in result:
            yield self(i)

    @classmethod
    def find_one(self, *args, **kwargs):
        result = self.get_collection().find_one(*args, **kwargs)
        if result:
            return self(result)
        else:
            return
            return

    @classmethod
    def ensure_index(self, *args, **kwargs):
        return self.get_collection().ensure_index

    @classmethod
    def create_index(self, *args, **kwargs):
        return self.get_collection().create_index

    @classmethod
    def serialize(self):
        import json
        data = TreeDict(self.structure)
        result = {}
        for key, value in data.iteritems():
            data_type = value.__class__.__name__
            result[key] = {'dataType': data_type, 
               'required': key in self.required_fields, 
               'options': value.get_options()}

        return json.dumps(result)