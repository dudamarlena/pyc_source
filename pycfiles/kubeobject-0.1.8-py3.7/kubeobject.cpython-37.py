# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kubeobject/kubeobject.py
# Compiled at: 2019-10-01 18:18:07
# Size of source mod 2**32: 8594 bytes
from __future__ import annotations
import yaml
from datetime import datetime, timedelta
from typing import Optional
from kubernetes import client

class CustomObject:
    __doc__ = 'CustomObject is an object mapping to a Custom Resource in Kubernetes. It\n    includes simple facilities to update the Custom Resource, save it and\n    reload its state in a object oriented manner.\n\n    It is meant to be used to apply changes to Custom Resources and watch their\n    state as it is updated by a controller; an Operator in Kubernetes parlance.\n\n    '

    def __init__--- This code section failed: ---

 L.  29         0  LOAD_FAST                'name'
                2  LOAD_FAST                'self'
                4  STORE_ATTR               name

 L.  30         6  LOAD_FAST                'namespace'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               namespace

 L.  32        12  LOAD_FAST                'plural'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     44  'to 44'
               20  LOAD_FAST                'kind'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_TRUE     44  'to 44'
               28  LOAD_FAST                'group'
               30  LOAD_CONST               None
               32  COMPARE_OP               is
               34  POP_JUMP_IF_TRUE     44  'to 44'
               36  LOAD_FAST                'version'
               38  LOAD_CONST               None
               40  COMPARE_OP               is
               42  POP_JUMP_IF_FALSE   106  'to 106'
             44_0  COME_FROM            34  '34'
             44_1  COME_FROM            26  '26'
             44_2  COME_FROM            18  '18'

 L.  33        44  LOAD_GLOBAL              get_crd_names
               46  LOAD_FAST                'plural'
               48  LOAD_FAST                'kind'
               50  LOAD_FAST                'group'
               52  LOAD_FAST                'version'
               54  LOAD_CONST               ('plural', 'kind', 'group', 'version')
               56  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               58  STORE_FAST               'crd'

 L.  34        60  LOAD_FAST                'crd'
               62  LOAD_ATTR                spec
               64  LOAD_ATTR                names
               66  LOAD_ATTR                kind
               68  LOAD_FAST                'self'
               70  STORE_ATTR               kind

 L.  35        72  LOAD_FAST                'crd'
               74  LOAD_ATTR                spec
               76  LOAD_ATTR                names
               78  LOAD_ATTR                plural
               80  LOAD_FAST                'self'
               82  STORE_ATTR               plural

 L.  36        84  LOAD_FAST                'crd'
               86  LOAD_ATTR                spec
               88  LOAD_ATTR                group
               90  LOAD_FAST                'self'
               92  STORE_ATTR               group

 L.  37        94  LOAD_FAST                'crd'
               96  LOAD_ATTR                spec
               98  LOAD_ATTR                version
              100  LOAD_FAST                'self'
              102  STORE_ATTR               version
              104  JUMP_FORWARD        130  'to 130'
            106_0  COME_FROM            42  '42'

 L.  39       106  LOAD_FAST                'kind'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               kind

 L.  40       112  LOAD_FAST                'plural'
              114  LOAD_FAST                'self'
              116  STORE_ATTR               plural

 L.  41       118  LOAD_FAST                'group'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               group

 L.  42       124  LOAD_FAST                'version'
              126  LOAD_FAST                'self'
              128  STORE_ATTR               version
            130_0  COME_FROM           104  '104'

 L.  46       130  LOAD_CONST               False
              132  LOAD_FAST                'self'
              134  STORE_ATTR               bound

 L.  50       136  LOAD_CONST               False
              138  LOAD_FAST                'self'
              140  STORE_ATTR               auto_save

 L.  55       142  LOAD_CONST               False
              144  LOAD_FAST                'self'
              146  STORE_ATTR               auto_reload

 L.  59       148  LOAD_GLOBAL              timedelta
              150  LOAD_CONST               2
              152  LOAD_CONST               ('seconds',)
              154  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              156  LOAD_FAST                'self'
              158  STORE_ATTR               auto_reload_period

 L.  62       160  LOAD_CONST               None
              162  LOAD_FAST                'self'
              164  STORE_ATTR               last_update

 L.  65       166  LOAD_GLOBAL              client
              168  LOAD_METHOD              CustomObjectsApi
              170  CALL_METHOD_0         0  '0 positional arguments'
              172  LOAD_FAST                'self'
              174  STORE_ATTR               api

 L.  67       176  LOAD_GLOBAL              hasattr
              178  LOAD_FAST                'self'
              180  LOAD_STR                 'backing_obj'
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  POP_JUMP_IF_TRUE    224  'to 224'

 L.  69       186  LOAD_FAST                'name'
              188  LOAD_FAST                'namespace'
              190  LOAD_CONST               ('name', 'namespace')
              192  BUILD_CONST_KEY_MAP_2     2 

 L.  70       194  LOAD_FAST                'self'
              196  LOAD_ATTR                kind

 L.  71       198  LOAD_STR                 '/'
              200  LOAD_METHOD              join
              202  LOAD_GLOBAL              filter
              204  LOAD_CONST               None
              206  LOAD_FAST                'group'
              208  LOAD_FAST                'version'
              210  BUILD_LIST_2          2 
              212  CALL_FUNCTION_2       2  '2 positional arguments'
              214  CALL_METHOD_1         1  '1 positional argument'
              216  LOAD_CONST               ('metadata', 'kind', 'apiVersion')
              218  BUILD_CONST_KEY_MAP_3     3 
              220  LOAD_FAST                'self'
              222  STORE_ATTR               backing_obj
            224_0  COME_FROM           184  '184'

Parse error at or near `JUMP_FORWARD' instruction at offset 104

    def load(self) -> 'CustomObject':
        """Loads this object from the API."""
        obj = self.api.get_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.name)
        self.backing_obj = obj
        self.bound = True
        self._register_updated
        return self

    def create(self) -> 'CustomObject':
        """Creates this object in Kubernetes."""
        obj = self.api.create_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.backing_obj)
        self.backing_obj = obj
        self.bound = True
        self._register_updated
        return self

    def update(self) -> 'CustomObject':
        """Updates the object in Kubernetes."""
        obj = self.api.patch_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.name, self.backing_obj)
        self.backing_obj = obj
        self._register_updated
        return self

    def _register_updated(self):
        """Register the last time the object was updated from Kubernetes."""
        self.last_update = datetime.now

    def _reload_if_needed(self):
        """Reloads the object is `self.auto_reload` is set to `True` and more than
        `self.auto_reload_period` time has passed since last reload."""
        if not self.auto_reload:
            return
        if self.last_update is None:
            self.reload
        if datetime.now - self.last_update > self.auto_reload_period:
            self.reload

    @classmethod
    def from_yaml(cls, yaml_file, name=None, namespace=None):
        """Creates a `CustomObject` from a yaml file. In this case, `name` and
        `namespace` are optional in this function's signature, because they
        might be passed as part of the `yaml_file` document.
        """
        doc = yaml.safe_loadopen(yaml_file)
        if 'metadata' not in doc:
            doc['metadata'] = dict()
        elif name is None or name == '':
            if 'name' not in doc['metadata']:
                raise ValueError('`name` needs to be passed as part of the function call or exist in the `metadata` section of the yaml document.')
            elif namespace is None or namespace == '':
                if 'namespace' not in doc['metadata']:
                    raise ValueError('`namespace` needs to be passed as part of the function call or exist in the `metadata` section of the yaml document.')
                elif name is None:
                    name = doc['metadata']['name']
                else:
                    doc['metadata']['name'] = name
                if namespace is None:
                    namespace = doc['metadata']['namespace']
            else:
                doc['metadata']['namespace'] = namespace
            kind = doc['kind']
            api_version = doc['apiVersion']
            if '/' in api_version:
                group, version = api_version.split'/'
            else:
                group = None
                version = api_version
            if getattr(cls, 'object_names_initialized', False):
                obj = cls(name, namespace)
        else:
            obj = cls(name, namespace, kind=kind, group=group, version=version)
        obj.backing_obj = doc
        return obj

    @classmethod
    def define(cls, name, kind=None, plural=None, group=None, version=None):
        """Defines a new class that will hold a particular type of object.

        This is meant to be used as a quick replacement for
        CustomObject if needed, but not extensive control or behaviour
        needs to be implemented. If your particular use case requires more
        control or more complex behaviour on top of the CustomObject class,
        consider subclassing it.
        """

        def __init__(self, name, namespace, **kwargs):
            CustomObject.__init__(self,
              name, namespace, kind=kind, plural=plural, group=group, version=version)

        def __repr__(self):
            return '{klass_name}({name}, {namespace})'.format(klass_name=name,
              name=(repr(self.name)),
              namespace=(repr(self.namespace)))

        return type(name, (
         CustomObject,), {'object_names_initialized':True, 
         '__init__':__init__, 
         '__repr__':__repr__})

    def delete(self):
        """Deletes the object from Kubernetes."""
        api = client.CustomObjectsApi
        body = client.V1DeleteOptions
        api.delete_namespaced_custom_object(self.group, self.version, self.namespace, self.plural, self.name, body)
        self._register_updated

    def reload(self):
        """Reloads the object from the Kubernetes API."""
        return self.load

    def __getitem__(self, key):
        self._reload_if_needed
        return self.backing_obj[key]

    def __contains__(self, key):
        self._reload_if_needed
        return key in self.backing_obj

    def __setitem__(self, key, val):
        self.backing_obj[key] = val
        if self.bound:
            if self.auto_save:
                self.update


def get_crd_names(plural=None, kind=None, group=None, version=None) -> 'Optional[dict]':
    """Gets the CRD entry that matches all the parameters passed."""
    api = client.ApiextensionsV1beta1Api
    if plural == kind  == group == version is None:
        return
    crds = api.list_custom_resource_definition
    for crd in crds.items:
        found = True
        if group != '':
            if crd.spec.group != group:
                found = False
        if version != '':
            if crd.spec.version != version:
                found = False
            elif kind is not None and crd.spec.names.kind != kind:
                found = False
            if plural is not None:
                if crd.spec.names.plural != plural:
                    found = False
            if found:
                return crd