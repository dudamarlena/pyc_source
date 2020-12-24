# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\Model.py
# Compiled at: 2018-01-18 12:27:56
# Size of source mod 2**32: 26796 bytes
import importlib, itertools, logging, os.path, re, sys
from .. import Document, Element
from ..exceptions import *
from ..publishsubscribe import Subscriber
from .decorators import *
from .exceptions import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='lang', type=('expatriate.model.xs.StringType',
                                                                                      'StringType'), into='_xml_lang')
@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='space', enum=('default',
                                                                                       'preserve'), into='_xml_space')
@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='base', type=('expatriate.model.xs.AnyUriType',
                                                                                      'AnyUriType'), into='_xml_base')
@attribute(namespace='http://www.w3.org/XML/1998/namespace', local_name='id', type=('expatriate.model.xs.IdType',
                                                                                    'IdType'), into='_xml_id')
@attribute(namespace='http://www.w3.org/2000/xmlns/', local_name='*', into='_xmlns')
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='type', type=('expatriate.model.xs.QNameType',
                                                                                           'QNameType'), into='_xsi_type')
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='nil', type=('expatriate.model.xs.BooleanType',
                                                                                          'BooleanType'), into='_xsi_nil', default=False)
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='schemaLocation', type=('expatriate.model.xs.AnyUriType',
                                                                                                     'AnyUriType'), into='_xsi_schemaLocation')
@attribute(namespace='http://www.w3.org/2001/XMLSchema-instance', local_name='noNamespaceSchemaLocation', type=('expatriate.model.xs.AnyUriType',
                                                                                                                'AnyUriType'), into='_xsi_noNamespaceSchemaLocation')
@content()
class Model(Subscriber):
    __doc__ = "\n    Base class for a XML object relation model. Allows mapping XML data into Python types.\n\n    :param local_name: Override for the xml local name when Model is generated.\n    :type local_name: str or None\n    :param namespace: Override for the xml namespace when Model is generated.\n    :type namespace: str or None\n    :param prefix: Override for the xml prefix when Model is generated.\n    :type prefix: str or None\n    :param value: Value to add to the Model's children (generated as CharacterData). No child is added if left as the default None.\n    :type local_name: str or None\n    :raises UnknownNamespaceException: if unable to determine a namespace model maps to\n    "
    ANY_NAMESPACE = '*'
    ANY_LOCAL_NAME = '*'
    _Model__namespace_to_package = {'http://www.w3.org/XML/1998/namespace':'expatriate.model.xml', 
     'http://www.w3.org/2001/XMLSchema':'expatriate.model.xs', 
     'http://www.w3.org/2001/XMLSchema-hasFacetAndProperty':'expatriate.model.xshfp', 
     'http://www.w3.org/2001/XMLSchema-instance':'expatriate.model.xsi'}
    _Model__namespace_to_prefix = {'http://www.w3.org/XML/1998/namespace':'xml', 
     'http://www.w3.org/2001/XMLSchema':'xs', 
     'http://www.w3.org/2001/XMLSchema-hasFacetAndProperty':'xshfp', 
     'http://www.w3.org/2001/XMLSchema-instance':'xsi'}
    _Model__package_to_namespace = {v:k for k, v in _Model__namespace_to_package.items()}
    _ns_count = 0
    _attribute_mappers = {}
    _attribute_mapper_cache = {}
    _element_mappers = {}
    _element_mapper_cache = {}
    _element_mapper_order = {}
    _content_mappers = {}
    _content_mapper_cache = {}

    def __init__(self, local_name=None, namespace=None, prefix=None, value=None):
        self._parent = None
        self._children = []
        if value is not None:
            self._children.append((None, value))
        else:
            self._local_name = local_name
            if namespace is not None:
                self._namespace = namespace
            else:
                self._namespace = Model.package_to_namespace(self.get_package())
            if self._namespace is None:
                raise UnknownNamespaceException('Unable to determine namespace for xml generation: ' + str(self))
            if prefix is not None:
                self._prefix = prefix
            else:
                self._prefix = Model.namespace_to_prefix(self._namespace)
        at_mappers = self._get_attribute_mappers()
        el_mappers = self._get_element_mappers()
        content_mappers = self._get_content_mappers()
        for mapper in itertools.chain(at_mappers, el_mappers, content_mappers):
            mapper.initialize(self)

        self._initialized = True

    @staticmethod
    def class_for_element(el):
        """
        load the model class corresponding to an element

        :param expatriate.Element el: The element for which to look up the class.
        :raises ElementMappingException: if class for element cannot be discovered
        """
        model_package = Model.namespace_to_package(el.namespace)
        try:
            pkg_mod = importlib.import_module(model_package)
        except:
            raise ElementMappingException('Unable to determine mapping for ' + str(el) + ' element: cannot load package module ' + model_package)

        try:
            class_name = pkg_mod.ELEMENT_MAP[(el.namespace, el.local_name)]
        except AttributeError:
            raise ElementMappingException(pkg_mod.__name__ + ' does not define ELEMENT_MAP; cannot load ' + str(el))
        except KeyError:
            raise ElementMappingException(pkg_mod.__name__ + ' does not define mapping for ' + str(el) + ' element')

        try:
            mod = importlib.import_module(model_package + '.' + class_name)
            class_ = getattr(mod, class_name)
        except:
            raise ElementMappingException('Unable to determine mapping for ' + str(el) + ' element: cannot load class module ' + model_package + '.' + class_name)

        return class_

    @classmethod
    def _get_attribute_mappers(cls):
        """
        get all the attribute definitions for a model class
        """
        if cls.__name__ not in Model._attribute_mapper_cache:
            mappers = []
            for cls_ in reversed(cls.__mro__):
                if issubclass(cls_, Model):
                    try:
                        logger.debug('Adding attribute mappers from superclass ' + cls_.__name__)
                        mappers.extend(cls_._attribute_mappers[cls_.__name__])
                    except KeyError:
                        pass

            Model._attribute_mapper_cache[cls.__name__] = mappers
        return Model._attribute_mapper_cache[cls.__name__]

    @classmethod
    def _add_attribute_mapper(cls, mapper):
        """
        set the model attribute definition for an attribute
        """
        if cls.__name__ not in cls._attribute_mappers:
            cls._attribute_mappers[cls.__name__] = []
        cls._attribute_mappers[cls.__name__].insert(0, mapper)

    @classmethod
    def _get_attribute_mapper_attr_names(cls):
        """
        get the attr names defined by the attribute mappers
        """
        names = []
        for mapper in cls._get_attribute_mappers():
            names.append(mapper.get_attr_name())

        return names

    @classmethod
    def _get_element_mappers(cls):
        """
        get all the element definitions for a model class
        """
        if cls.__name__ not in Model._element_mapper_cache:
            mappers = []
            for cls_ in reversed(cls.__mro__):
                if issubclass(cls_, Model):
                    try:
                        logger.debug('Adding element mappers from superclass ' + cls_.__name__)
                        mappers.extend(cls_._element_mappers[cls_.__name__])
                    except KeyError:
                        pass

            Model._element_mapper_cache[cls.__name__] = mappers
        return Model._element_mapper_cache[cls.__name__]

    @classmethod
    def _add_element_mapper(cls, mapper):
        """
        set the model element definition for an element
        """
        if cls.__name__ not in cls._element_mappers:
            cls._element_mappers[cls.__name__] = []
        cls._element_mappers[cls.__name__].insert(0, mapper)
        if cls.__name__ not in cls._element_mapper_order:
            cls._element_mapper_order[cls.__name__] = []
        cls._element_mapper_order[cls.__name__].insert(0, (
         mapper.get_namespace(), mapper.get_local_name()))

    @classmethod
    def _get_element_mapper_attr_names(cls):
        """
        get the attr names defined by the element mappers
        """
        names = []
        for mapper in cls._get_element_mappers():
            names.append(mapper.get_attr_name())

        return names

    @classmethod
    def _add_content_mapper(cls, mapper):
        """
        add a model content definition for the class
        """
        if cls.__name__ not in cls._content_mappers:
            cls._content_mappers[cls.__name__] = []
        cls._content_mappers[cls.__name__].insert(0, mapper)

    @classmethod
    def _get_content_mappers(cls):
        """
        get the model content definitions
        """
        if cls.__name__ not in Model._content_mapper_cache:
            mappers = []
            for cls_ in reversed(cls.__mro__):
                if issubclass(cls_, Model):
                    try:
                        logger.debug('Adding content mappers from superclass ' + cls_.__name__)
                        mappers.extend(cls_._content_mappers[cls_.__name__])
                    except KeyError:
                        pass

            Model._content_mapper_cache[cls.__name__] = mappers
        return Model._content_mapper_cache[cls.__name__]

    @staticmethod
    def register_namespace(model_package, namespace, prefix=None):
        """
        Register a namespace for use

        :param str model_package: The package to use for mapping elements from namespace
        :param str namespace: The namespace
        :param prefix: The prefix to use when mapping to namespace
        :type prefix: str or None
        """
        Model._Model__namespace_to_package[namespace] = model_package
        Model._Model__package_to_namespace[model_package] = namespace
        Model._Model__namespace_to_prefix[namespace] = prefix

    @staticmethod
    def unregister_namespace(model_package):
        """
        Unregister a namespace.

        :param str model_package: The package to unregister from mapping
        :raises UnknownNamespaceException: if the namspace isn't registered
        """
        try:
            namespace = Model._Model__package_to_namespace[model_package]
        except KeyError:
            raise UnknownNamespaceException('Unregistered namespace: ' + model_package)

        del Model._Model__package_to_namespace[model_package]
        del Model._Model__namespace_to_package[namespace]
        del Model._Model__namespace_to_prefix[namespace]

    @staticmethod
    def package_to_namespace(model_package):
        """
        Find namespace corresponding to a model package.

        :param str model_package: The package to lookup
        :raises UnknownNamespaceException: if the package isn't registered
        """
        logger.debug('Looking for xml namespace for model package ' + model_package)
        if model_package not in Model._Model__package_to_namespace:
            raise UnknownNamespaceException('Package ' + model_package + ' is not in registered packages')
        return Model._Model__package_to_namespace[model_package]

    @staticmethod
    def namespace_to_package(namespace):
        """
        Find model package corresponding to namespace.

        :param str namespace: The namespace to lookup
        :raises UnknownNamespaceException: if the namspace isn't registered
        """
        logger.debug('Looking for model package for xml namespace ' + str(namespace))
        if namespace not in Model._Model__namespace_to_package:
            raise UnknownNamespaceException('XML namespace ' + str(namespace) + ' is not in registered namespaces')
        return Model._Model__namespace_to_package[namespace]

    @staticmethod
    def namespace_to_prefix(namespace):
        """
        Find the model package corresponding to a namespace.

        :param str namespace: The namespace to lookup
        :raises UnknownNamespaceException: if the namspace isn't registered
        """
        logger.debug('Looking for xml prefix for xml namespace ' + str(namespace))
        prefix = None
        try:
            prefix = Model._Model__namespace_to_prefix[namespace]
        except KeyError:
            prefix = 'ns' + str(Model._ns_count)
            Model._ns_count += 1
            logger.info(pkg_mod.__name__ + ' did not register prefix; generated: ' + prefix)
        except:
            raise UnknownNamespaceException('Unable to determine prefix for ' + namespace + ' namespace')

        return prefix

    @classmethod
    def get_package(cls):
        """
        Find package corresponding to class/instance

        :rtype: str
        """
        return cls.__module__.rpartition('.')[0]

    @staticmethod
    def load(parent, el):
        """
        load a Model given an expatriate Element

        :param expatriate.model.Model parent: The :py:class:`.Model` to use as the parent of the model we're mapping from el
        :param expatriate.Element el: The :py:class:`..Element` from which we're mapping
        """
        if parent is None:
            if el.namespace is None:
                raise UnknownNamespaceException('Unable to determine namespace without fully qualified element (' + str(el) + ') and parent model')
            class_ = Model.class_for_element(el)
        else:
            logger.debug('Checking ' + parent.__class__.__name__ + ' for element ' + str(el))
            for mapper in parent._get_element_mappers():
                if mapper.matches(el, parent):
                    logger.debug(str(el) + ' matched ' + str(mapper) + ' in ' + parent.__class__.__name__)
                    class_ = mapper.class_for_element(el, parent)
                    break
            else:
                raise ElementMappingException(parent.__class__.__name__ + ' does not define mapping for ' + str(el) + ' element')

        logger.debug('Loaded class ' + str(class_) + ' for ' + str(el))
        inst = class_()
        inst.parse(parent, el)
        return inst

    @staticmethod
    def find_content(uri):
        """
        Loads the content from the URI, parses it, returns the root Model.
        Remote URIs are not yet supported.

        :param str uri: The URI to load
        :rtype: .Model or subclass
        :raises ReferenceException: if the content could not be found
        """
        if os.path.isfile(uri):
            try:
                doc = Document()
                doc.parse_file(uri)
                return Model.load(None, doc.root_element)
            except:
                raise ReferenceException('Could not find content for: ' + uri)

        else:
            raise NotImplementedError('Remote URI loading is not yet implemented')
        raise ReferenceException('Could not find content for: ' + uri)

    def __setattr__(self, name, value):
        """
        setattr override to keep track of indexes etc.
        """
        if not hasattr(self, '_initialized'):
            object.__setattr__(self, name, value)
            return
        el_mappers = self._get_element_mappers()
        for mapper in itertools.chain(el_mappers):
            if mapper.get_attr_name() == name:
                mapper.setattr(self, name, value)
                return

        object.__setattr__(self, name, value)

    def _attr_name_from_publisher(self, publisher):
        for k, v in self.__dict__.items():
            if publisher == v:
                return k

        raise AttributeError('Attribute matching ' + str(publisher) + ' not found')

    def _data_added(self, publisher, id_, item):
        pub_name = self._attr_name_from_publisher(publisher)
        self._children.append((pub_name, id_))

    def _data_updated(self, publisher, id_, old_item, new_item):
        pass

    def _data_deleted(self, publisher, id_, item):
        pub_name = self._attr_name_from_publisher(publisher)
        self._children.remove((pub_name, id_))
        if isinstance(publisher, list):
            new_children = []
            for attr_name, idx in self._children:
                if pub_name == attr_name and isinstance(idx, int) and idx > id_:
                    new_children.append((attr_name, idx - 1))
                else:
                    new_children.append((attr_name, idx))

            object.__setattr__(self, '_children', new_children)

    def is_nil(self):
        """
        Determine if the model's xsi nil is set

        :rtype: bool
        """
        return self._xsi_nil

    def set_nil(self):
        """
        Set model's xsi nil and clear the value.
        """
        self._xsi_nil = True
        self.set_value(None)

    def _get_content_children(self):
        """
        Get the content children of the model
        """
        content = []
        for attr_name, id_ in self._children:
            if attr_name is None:
                content.append(id_)

        return content

    def get_value(self):
        """
        Get the joined str value of the model's children

        :rtype: str
        """
        content = self._get_content_children()
        if len(content) == 0:
            return
        else:
            return ''.join(content)

    def set_value(self, value):
        """
        Set content to *value*. Effectively clears all content children and
        appends the *value*.

        :param str value: The str value
        """
        new_children = []
        for attr_name, id_ in self._children:
            if attr_name is not None:
                new_children.append((attr_name, id_))

        self._children = new_children
        if value is not None:
            self._children.append((None, value))

    def parse_value(self, value):
        r"""
        Parse the given *value* and return; overriden for value-limiting
        subclasses (most of the :py:mod:`expatriate.model.xs` \*Type classes)

        For example :py:class:`expatriate.model.xs.FloatType` parses a
        :py:class:`str` value and returns a :py:class:`float` type

        :param value: The value to be parsed
        """
        return value

    def produce_value(self, value):
        r"""
        produce the given *value* and return; overriden for value-limiting
        subclasses (most of the :py:mod:`expatriate.model.xs` \*Type classes)

        For example :py:class:`expatriate.model.xs.FloatType` produces a
        :py:class:`str` type from a :py:class:`float` value

        :param value: The value produced
        """
        if value is None:
            return value
        else:
            return str(value)

    def __str__(self):
        s = self.__class__.__name__
        if hasattr(self, 'id'):
            if self.id is not None:
                s += ' id: ' + self.id
        elif hasattr(self, 'Id'):
            if self.Id is not None:
                s += ' Id: ' + self.Id
        elif hasattr(self, 'name'):
            if self.name is not None:
                s += ' name: ' + self.name
        else:
            s += ' # ' + str(id(self))
        return s

    def find_reference(self, ref):
        """
        Find child that matches reference *ref*. A child matches if it has an
        attribute *id* that is equal to the ref argument.

        :param str ref: The reference to a child for which to search this model recursively
        :rtype: .Model
        """
        logger.debug('Matching reference ' + ref + ' against ' + str(self))
        try:
            if self.id == ref:
                return self
        except AttributeError:
            pass

        for mapper in self._get_element_mappers():
            try:
                return mapper.find_reference_in(ref, self)
            except ReferenceException:
                pass

        raise ReferenceException('Could not find reference ' + ref + ' within ' + str(self))

    def parse(self, parent, el):
        """
        Load model data from xml element *el*

        :param .Model parent: The parent of the model being parsed
        :param expatriate.Element el: The element being parsed into the model
        """
        self._parent = parent
        self._local_name = el.local_name
        self._namespace = el.namespace
        self._prefix = el.prefix
        logger.debug('Parsing ' + str(el) + ' element into ' + self.__class__.__module__ + '.' + self.__class__.__name__ + ' class')
        for name, attr in el.attribute_nodes.items():
            for mapper in self._get_attribute_mappers():
                if mapper.matches(attr, self):
                    mapper.parse_in(self, attr)
                    break
            else:
                raise UnknownAttributeException('Unknown ' + str(self) + ' attribute ' + str(attr))

        for child in el.children:
            if isinstance(child, Element):
                for mapper in self._get_element_mappers():
                    if mapper.matches(child, self):
                        mapper.parse_in(self, child)
                        break
                else:
                    raise UnknownElementException('Unknown ' + str(self) + ' child ' + str(child) + ' does not match any mappers')

            else:
                self._children.append((None, child.get_string_value()))

        at_mappers = self._get_attribute_mappers()
        el_mappers = self._get_element_mappers()
        content_mappers = self._get_content_mappers()
        for mapper in itertools.chain(at_mappers, el_mappers, content_mappers):
            mapper.validate(self)

    def produce(self, parent_el=None):
        """
        Generate xml from the model

        :param expatriate.Element parent_el: The expatriate.Element to use as the parent of the element generated from this model
        :rtype: expatriate.Element
        """
        logger.debug(str(self) + ' to xml')
        at_mappers = self._get_attribute_mappers()
        el_mappers = self._get_element_mappers()
        content_mappers = self._get_content_mappers()
        for mapper in itertools.chain(at_mappers, el_mappers, content_mappers):
            mapper.validate(self)

        if self._local_name is None:
            raise ElementMappingException('local_name must be defined by constructor or @element')
        el = Element((self._local_name), namespace=(self._namespace), prefix=(self._prefix), parent=parent_el)
        for mapper in at_mappers:
            mapper.produce_in(el, self)

        for attr_name, id_ in self._children:
            if attr_name is None:
                for mapper in content_mappers:
                    mapper.produce_in(el, self, id_)

            else:
                for mapper in el_mappers:
                    if attr_name == mapper.get_attr_name():
                        mapper.produce_in(el, self, id_)
                        break
                else:
                    raise ElementMappingException('Unable to map ' + str(self) + ' attribute ' + attr_name + str([id_]) + ' to element')

        return el