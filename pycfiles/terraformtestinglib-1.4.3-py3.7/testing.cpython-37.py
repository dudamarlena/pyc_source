# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/terraformtestinglib/terraformtestinglib/testing/testing.py
# Compiled at: 2019-10-22 09:06:10
# Size of source mod 2**32: 32680 bytes
"""
Main code for testing.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import functools, json, logging, re, typing
from operator import attrgetter
from dataclasses import dataclass
from terraformtestinglib.terraformtestinglib import Parser
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'testing'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

def assert_on_error(func):
    """Raises assertion error exceptions if the wrapped method returned any errors."""

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        value, errors = func(*args, **kwargs)
        if errors:
            raise AssertionError('\n\t' + '\n\t'.join(sorted(errors)))
        return value

    return wrapped


@dataclass
class Entity:
    __doc__ = 'Basic model of an entity exposing required attributes.'
    type: str
    name: str
    data: typing.Any


@dataclass
class Resource(Entity):
    __doc__ = 'Basic model of a resource exposing required attributes.'


@dataclass
class Data(Entity):
    __doc__ = 'Basic model of a data object exposing required attributes.'


@dataclass
class Provider(Entity):
    __doc__ = 'Basic model of a provider object exposing required attributes.'


@dataclass
class Terraform(Entity):
    __doc__ = 'Basic model of a provider object exposing required attributes.'


class Validator(Parser):
    __doc__ = 'Object exposing resources and variables of terraform plans.'

    def __init__(self, configuration_path, global_variables_file_path=None, raise_on_missing_variable=True, environment_variables=None):
        super(Validator, self).__init__(configuration_path, global_variables_file_path, raise_on_missing_variable, environment_variables)
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.error_on_missing_attribute = False

    def resources(self, type_):
        """Filters resources based on resource type which is always cast to list.

        Args:
            type_ (basestring|list): The type of resources to filter on. Always gets cast to a list.

        Returns:
            ResourceList : An object containing the resources matching the type provided

        """
        resource_types = self.to_list(type_)
        resources = []
        for resource_type, resource in self.hcl_view.resources.items():
            if resource_type in resource_types:
                for resource_name, resource_data in resource.items():
                    if resource_data.get('tags', {}).get('skip-testing'):
                        self._logger.warning('Skipping resource %s testing due to user overriding tag.', resource_name)
                    else:
                        resources.append(Resource(resource_type, resource_name, resource_data))

        return ResourceList(self, sorted(resources, key=(attrgetter('name'))))

    def data(self, type_):
        """Filters data based on data type which is always cast to list.

        Args:
            type_ (basestring|list): The type of data attributes to filter on. Always gets cast to a list.

        Returns:
            DataList : An object containing the data matching the type provided

        """
        return self._entity('data', Data, DataList, type_)

    def provider(self, type_):
        """Filters providers based on provider type which is always cast to list.

        Args:
            type_ (basestring|list): The type of provider to filter on. Always gets cast to a list.

        Returns:
            ProviderList : An object containing the providers matching the type provided

        """
        return self._entity('provider', Provider, ProviderList, type_)

    def terraform(self, type_):
        """Filters terraform entries based on provided type which is always cast to list.

        Args:
            type_ (basestring|list): The type of terraform attributes to filter on. Always gets cast to a list.

        Returns:
            TerraformList : An object containing the terraform objects matching the type provided

        """
        return self._entity('terraform', Terraform, TerraformList, type_)

    def _entity(self, state_object, entity_object, entity_container, entity_type):
        types = self.to_list(entity_type)
        output_list = []
        for _type, data in getattr(self.hcl_view, state_object).items():
            if _type in types:
                output_list.append(entity_object(_type, _type, data))

        return entity_container(self, sorted(output_list, key=(attrgetter('name'))))

    def variable(self, name):
        """Returns a variable object of the provided name.

        Args:
            name (basestring): The name of the variable to retrieve

        Returns:
            Variable : An object modeling a variable

        """
        return Variable(name, self.hcl_view.state.get('variable', {}).get(name))

    def get_variable_value(self, variable):
        """Retrieves the variable value from the global view state.

        Args:
            variable (basestring): The variable to retrieve the value for

        Returns:
            value : The value of the retrieved variable

        """
        return self.hcl_view.get_variable_value(variable)

    @staticmethod
    def to_list(value):
        """Casts to list the provided argument if not a list already.

        Args:
            value (basestring|list): Casts the provided value to list if not already

        Returns:
            value (list) : A list of the value or values

        """
        if not isinstance(value, (tuple, list)):
            value = [
             value]
        return value


class Container:
    __doc__ = 'An object handling the exposing of attributes of different resources of terraform.'

    def __init__(self, validator_instance, entities):
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.validator = validator_instance
        self._Container__entities = entities

    @property
    def _entities(self):
        return self._Container__entities

    @assert_on_error
    def attribute--- This code section failed: ---

 L. 250         0  BUILD_LIST_0          0 
                2  STORE_FAST               'errors'

 L. 251         4  BUILD_LIST_0          0 
                6  STORE_FAST               'attributes_list'

 L. 252         8  SETUP_LOOP          202  'to 202'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                _entities
               14  GET_ITER         
             16_0  COME_FROM           162  '162'
               16  FOR_ITER            200  'to 200'
               18  STORE_FAST               'entity'

 L. 253        20  LOAD_GLOBAL              isinstance
               22  LOAD_FAST                'entity'
               24  LOAD_ATTR                data
               26  LOAD_GLOBAL              dict
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  POP_JUMP_IF_TRUE     54  'to 54'

 L. 254        32  LOAD_FAST                'attributes_list'
               34  LOAD_METHOD              append
               36  LOAD_GLOBAL              Attribute
               38  LOAD_FAST                'entity'
               40  LOAD_FAST                'name'
               42  LOAD_FAST                'entity'
               44  LOAD_ATTR                data
               46  CALL_FUNCTION_3       3  '3 positional arguments'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  POP_TOP          

 L. 255        52  CONTINUE             16  'to 16'
             54_0  COME_FROM            30  '30'

 L. 256        54  LOAD_FAST                'name'
               56  LOAD_FAST                'entity'
               58  LOAD_ATTR                data
               60  LOAD_METHOD              keys
               62  CALL_METHOD_0         0  '0 positional arguments'
               64  COMPARE_OP               in
               66  POP_JUMP_IF_FALSE   156  'to 156'

 L. 257        68  LOAD_GLOBAL              isinstance
               70  LOAD_FAST                'entity'
               72  LOAD_ATTR                data
               74  LOAD_METHOD              get
               76  LOAD_FAST                'name'
               78  CALL_METHOD_1         1  '1 positional argument'
               80  LOAD_GLOBAL              list
               82  CALL_FUNCTION_2       2  '2 positional arguments'
               84  POP_JUMP_IF_FALSE   128  'to 128'

 L. 258        86  SETUP_LOOP          154  'to 154'
               88  LOAD_FAST                'entity'
               90  LOAD_ATTR                data
               92  LOAD_METHOD              get
               94  LOAD_FAST                'name'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  GET_ITER         
              100  FOR_ITER            124  'to 124'
              102  STORE_FAST               'entry'

 L. 259       104  LOAD_FAST                'attributes_list'
              106  LOAD_METHOD              append
              108  LOAD_GLOBAL              Attribute
              110  LOAD_FAST                'entity'
              112  LOAD_FAST                'name'
              114  LOAD_FAST                'entry'
              116  CALL_FUNCTION_3       3  '3 positional arguments'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  POP_TOP          
              122  JUMP_BACK           100  'to 100'
              124  POP_BLOCK        
              126  JUMP_ABSOLUTE       198  'to 198'
            128_0  COME_FROM            84  '84'

 L. 261       128  LOAD_FAST                'attributes_list'
              130  LOAD_METHOD              append
              132  LOAD_GLOBAL              Attribute
              134  LOAD_FAST                'entity'
              136  LOAD_FAST                'name'
              138  LOAD_FAST                'entity'
              140  LOAD_ATTR                data
              142  LOAD_METHOD              get
              144  LOAD_FAST                'name'
              146  CALL_METHOD_1         1  '1 positional argument'
              148  CALL_FUNCTION_3       3  '3 positional arguments'
              150  CALL_METHOD_1         1  '1 positional argument'
              152  POP_TOP          
            154_0  COME_FROM_LOOP       86  '86'
              154  JUMP_BACK            16  'to 16'
            156_0  COME_FROM            66  '66'

 L. 262       156  LOAD_FAST                'self'
              158  LOAD_ATTR                validator
              160  LOAD_ATTR                error_on_missing_attribute
              162  POP_JUMP_IF_FALSE    16  'to 16'

 L. 263       164  LOAD_FAST                'errors'
              166  LOAD_METHOD              append
              168  LOAD_STR                 '['
              170  LOAD_FAST                'entity'
              172  LOAD_ATTR                type
              174  FORMAT_VALUE          0  ''
              176  LOAD_STR                 '.'
              178  LOAD_FAST                'entity'
              180  LOAD_ATTR                name
              182  FORMAT_VALUE          0  ''
              184  LOAD_STR                 "] should have attribute: '"
              186  LOAD_FAST                'name'
              188  FORMAT_VALUE          0  ''
              190  LOAD_STR                 "'"
              192  BUILD_STRING_7        7 
              194  CALL_METHOD_1         1  '1 positional argument'
              196  POP_TOP          
              198  JUMP_BACK            16  'to 16'
              200  POP_BLOCK        
            202_0  COME_FROM_LOOP        8  '8'

 L. 264       202  LOAD_GLOBAL              AttributeList
              204  LOAD_FAST                'self'
              206  LOAD_ATTR                validator
              208  LOAD_FAST                'attributes_list'
              210  CALL_FUNCTION_2       2  '2 positional arguments'
              212  LOAD_FAST                'errors'
              214  BUILD_TUPLE_2         2 
              216  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 154_0

    @assert_on_error
    def attribute_matching_regex(self, regex):
        """Filters attributes based on the provided regex.

        Args:
            regex (basestring): A basestring of a valid regular expression to match against

        Raises:
            AssertionError : If any errors are calculated

        Returns:
            AttributeList (list) : An object containing any attributes matching the check

        """
        errors = []
        attributes_list = []
        for resource in self._entities:
            matched = False
            for attribute in resource.data.keys():
                if re.search(regex, attribute):
                    attributes_list.append(Attribute(resource, attribute, resource.data.get(attribute)))
                    matched = True

            if self.validator.error_on_missing_attribute:
                matched or errors.append(f"[{resource.type}.{resource.name}] should have attribute matching regex: '{regex}'")

        return (
         AttributeList(self.validator, attributes_list), errors)

    @assert_on_error
    def should_have_attributes(self, attributes_list):
        """Validates that the resource has the provided arguments which are always cast to a list.

        Args:
            attributes_list (list): A list of strings for attributes to check against

        Raises:
            AssertionError : If any errors are calculated

        Returns:
            None

        """
        attributes_list = self.validator.to_list(attributes_list)
        errors = []
        for resource in self._entities:
            for attribute in attributes_list:
                if attribute not in resource.data.keys():
                    errors.append(f"[{resource.type}.{resource.name}] should have attribute: '{attribute}'")

        return (
         None, errors)

    @assert_on_error
    def should_not_have_attributes(self, attributes_list):
        """Validates that the resource does not have the provided arguments which are always cast to a list.

        Args:
            attributes_list (list): A list of strings for attributes to check against

        Raises:
            AssertionError : If any errors are calculated

        Returns:
            None

        """
        attributes_list = self.validator.to_list(attributes_list)
        errors = []
        for resource in self._entities:
            for attribute in attributes_list:
                if attribute in resource.data.keys():
                    errors.append(f"[{resource.type}.{resource.name}] should not have attribute(s): '{attribute}'")

        return (
         None, errors)

    def if_has_attribute(self, attribute):
        """Filters the entities based on the provided attribute.

        Args:
            attribute (basestring): The attribute to filter the resources on

        Returns:
             (list) : An entities list object with all resources following the pattern

        """
        entities = []
        for entity in self._entities:
            if attribute in entity.data.keys():
                entities.append(entity)

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_not_has_attribute(self, attribute):
        """Filters the entities based on the non existence of the provided attribute.

        Args:
            attribute (basestring): The attribute to filter the resources on

        Returns:
            (list)) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            if attribute not in entity.data.keys():
                entities.append(entity)

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_has_attribute_with_value(self, attribute, value):
        """Filters the entities based on the provided attribute and value.

        Args:
            attribute (basestring): The attribute to filter the entities on
            value : The value to match with

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            if attribute in entity.data.keys():
                attribute_value = entity.data.get(attribute)
                if attribute_value == value:
                    entities.append(entity)

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_not_has_attribute_with_value(self, attribute, value):
        """Filters the entities based on the provided attribute and value.

        Args:
            attribute (basestring): The attribute to filter the resources on
            value : The value to not match

        Returns:
            (list)) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            if attribute in entity.data.keys():
                attribute_value = entity.data.get(attribute)
                attribute_value == value or entities.append(entity)

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_has_attribute_with_regex_value(self, attribute, regex):
        """Filters the entities based on the provided attribute and value.

        Args:
            attribute (basestring): The attribute to filter the entities on if the value matches the regex provided
            regex : The regex to match with

        Returns:
            (list)) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            if attribute in entity.data.keys():
                attribute_value = entity.data.get(attribute)
                try:
                    if re.search(regex, attribute_value):
                        entities.append(entity)
                except TypeError:
                    pass

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_not_has_attribute_with_regex_value(self, attribute, regex):
        """Filters the entities based on the provided attribute and value.

        Args:
            attribute (basestring): The attribute to filter the entities on if the value does not match the regex
            regex : The regex not to match with

        Returns:
            (list)) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            if attribute in entity.data.keys():
                attribute_value = entity.data.get(attribute)
                try:
                    if not re.search(regex, attribute_value):
                        entities.append(entity)
                except TypeError:
                    pass

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_has_subattribute(self, parent_attribute, attribute):
        """Filters the entities based on the provided parent and child attribute.

        Args:
            parent_attribute (basestring): The parent attribute to filter the resources on
            attribute (basestring): The child attribute to filter the entities on if it exists

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            parent = entity.data.get(parent_attribute, {})
            if parent.get(attribute):
                entities.append(entity)

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_not_has_subattribute(self, parent_attribute, attribute):
        """Filters the entities based on the provided parent and child attribute.

        Args:
            parent_attribute (basestring): The parent attribute to filter the entities on
            attribute (basestring): The child attribute to filter the entities on if it does not exists

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            parent = entity.data.get(parent_attribute, {})
            if not parent.get(attribute):
                entities.append(entity)

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_has_subattribute_with_value(self, parent_attribute, attribute, value):
        """Filters the entities based on the provided parent and child attribute and value.

        Args:
            parent_attribute (basestring): The parent attribute to filter the entities on
            attribute (basestring): The child attribute to filter the entities on
            value : The value to match with for the child attribute

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            parent = entity.data.get(parent_attribute, {})
            try:
                if value == parent.get(attribute):
                    entities.append(entity)
            except TypeError:
                pass

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_not_has_subattribute_with_value(self, parent_attribute, attribute, value):
        """Filters the entities based on the provided parent and child attribute and value.

        Args:
            parent_attribute (basestring): The parent attribute to filter the entities on
            attribute (basestring): The child attribute to filter the entities on
            value : The value to not match with for the child attribute

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            parent = entity.data.get(parent_attribute, {})
            try:
                if not value == parent.get(attribute):
                    entities.append(entity)
            except TypeError:
                pass

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_has_subattribute_with_regex_value(self, parent_attribute, attribute, regex):
        """Filters the entities based on the provided parent and child attribute and regex for value matching.

        Args:
            parent_attribute (basestring): The parent attribute to filter the entities on
            attribute (basestring): The child attribute to filter the entities on
            regex : The regex to match with for the child attribute's value

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            parent = entity.data.get(parent_attribute, {})
            try:
                if re.search(regex, parent.get(attribute)):
                    entities.append(entity)
            except TypeError:
                pass

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))

    def if_not_has_subattribute_with_regex_value(self, parent_attribute, attribute, regex):
        """Filters the entities based on the provided parent and child attribute and regex for value matching.

        Args:
            parent_attribute (basestring): The parent attribute to filter the entities on
            attribute (basestring): The child attribute to filter the entities on
            regex : The regex to not match with for the child attribute's value

        Returns:
            (list) : An entities list object with all entities following the pattern

        """
        entities = []
        for entity in self._entities:
            parent = entity.data.get(parent_attribute, {})
            try:
                if not re.search(regex, parent.get(attribute)):
                    entities.append(entity)
            except TypeError:
                pass

        return self.__class__(self.validator, sorted(entities, key=(attrgetter('name'))))


class DataList(Container):
    __doc__ = 'A list of data objects being capable to filter on specific requirements.'


class ProviderList(Container):
    __doc__ = 'A list of provider objects being capable to filter on specific requirements.'


class TerraformList(Container):
    __doc__ = 'A list of terraform objects being capable to filter on specific requirements.'


class ResourceList(Container):
    __doc__ = 'A list of resource objects being capable to filter on specific requirements.'

    def resources(self, type_):
        """Filters resources based on resource type which is always cast to list.

        Args:
            type_ (list|basestring): The type of resources to filter on. Always gets cast to list.

        Raises:
            AssertionError : If any errors are calculated

        Returns:
            ResourceList (list) : An object containing any resources matching the type

        """
        resource_types = self.validator.to_list(type_)
        resources = []
        for resource in self._entities:
            if resource.type in resource_types:
                resources.append(resource)

        return ResourceList(self.validator, sorted(resources, key=(attrgetter('name'))))


class AttributeList:
    __doc__ = 'Object containing attribute objects and providing validation methods for them.'

    def __init__(self, validator, attributes):
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.validator = validator
        self.attributes = attributes

    @assert_on_error
    def attribute(self, name):
        """Filters attributes on matching the provided name.

        Args:
            name ( basestring): The name to match the attribute with

        Returns:
            AttributeList : A container of attribute objects

        """
        errors = []
        attributes = []
        for attribute in self.attributes:
            if isinstance(attribute.value, list):
                for entry in attribute.value:
                    attributes.append(Attribute(attribute._resource, f"{attribute.name}.{name}", entry))

            elif name in attribute.value.keys():
                attributes.append(Attribute(attribute._resource, f"{attribute.name}.{name}", attribute.value[name]))
            elif self.validator.error_on_missing_attribute:
                errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] should have attribute: '{attribute.name}'")

        return (
         AttributeList(self.validator, attributes), errors)

    @assert_on_error
    def should_equal(self, value):
        """Checks for equality for the provided value from all contained attributes.

        Args:
            value : The value to match with

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        for attribute in self.attributes:
            if not attribute.value == value:
                errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] should be '{value}'. Is: '{attribute.value}'")

        return (
         None, errors)

    def if_has_attribute_with_value(self, attribute, value):
        """Filters the AttributeList based on the provided attribute and value.

        Args:
            attribute: The attribute to filter on
            value: the value of the attribute to filter on

        Returns:
            AttributeList : A container of attribute objects

        """
        attributes = []
        for attribute_ in self.attributes:
            try:
                if value == attribute_.value.get(attribute):
                    attributes.append(attribute_)
            except TypeError:
                pass

        return AttributeList(self.validator, attributes)

    def if_not_has_attribute_with_value(self, attribute, value):
        """Filters the AttributeList based on the provided attribute and value.

        Args:
            attribute: The attribute to filter on
            value: the value of the attribute to filter on

        Returns:
            AttributeList : A container of attribute objects

        """
        attributes = []
        for attribute_ in self.attributes:
            try:
                if not value == attribute_.value.get(attribute):
                    attributes.append(attribute_)
            except TypeError:
                pass

        return AttributeList(self.validator, attributes)

    @assert_on_error
    def should_not_equal(self, value):
        """Checks for inequality for the provided value from all contained attributes.

        Args:
            value : The value to not match with

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        for attribute in self.attributes:
            if attribute.value == value:
                errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] should not be '{value}'. Is: '{attribute.value}'")

        return (
         None, errors)

    @assert_on_error
    def should_have_attributes(self, attributes):
        """Checks for existence for the provided attribute from all contained attributes.

        Args:
            attributes : An attribute or list of attributes to check for

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        for attribute in self.attributes:
            for provided_attribute in self.validator.to_list(attributes):
                if provided_attribute not in attribute.value.keys():
                    errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] should have attribute: '{provided_attribute}'")

        return (
         None, errors)

    @assert_on_error
    def should_not_have_attributes(self, attributes):
        """Checks for lack for the provided attribute from all contained attributes.

        Args:
            attributes : An attribute or list of attributes to check for

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        attributes = self.validator.to_list(attributes)
        for attribute in self.attributes:
            for required_property_name in attributes:
                if required_property_name in attribute.value.keys():
                    errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] should not have attribute: '{required_property_name}'")

        return (
         None, errors)

    @assert_on_error
    def should_match_regex(self, regex):
        """Checks for regular expression match from all contained attributes.

        Args:
            regex (basestring) : A regular expression to match with

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        for attribute in self.attributes:
            try:
                if not re.search(regex, attribute.value):
                    errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] with value '{attribute.value}' should match regex '{regex}'")
            except (ValueError, TypeError, AttributeError):
                errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] with value '{attribute.value}' should match regex '{regex}'")

        return (
         None, errors)

    @assert_on_error
    def should_not_match_regex(self, regex):
        """Checks for regular expression not matching from all contained attributes.

        Args:
            regex (basestring) : A regular expression to not match with

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        for attribute in self.attributes:
            if re.search(regex, attribute.value):
                errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] with value '{attribute.value}' should not match regex '{regex}'")

        return (
         None, errors)

    @assert_on_error
    def should_be_valid_json(self):
        """Checks whether the value for the attribute is valid json.

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        errors = []
        for attribute in self.attributes:
            try:
                json.loads(attribute.value)
            except (ValueError, TypeError, AttributeError):
                errors.append(f"[{attribute.resource_type}.{attribute.resource_name}.{attribute.name}] is not valid json")

        return (
         None, errors)


class Variable:
    __doc__ = 'Models a variable and exposes basic test for it.'

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def value_exists(self):
        """Checks that the value exists.

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        assert self.value, f"Variable '{self.name}' should have a default value"

    def value_equals(self, value):
        """Checks that the value equals the provided value.

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        assert self.value == value, f"Variable '{self.name}' should have a default value of {value}. Is: {self.value}"

    def value_matches_regex(self, regex):
        """Checks that the value matches the provided regex.

        Raises:
            AssertionError : If any errors are found on the check

        Returns:
            None

        """
        assert re.search(regex, self.value), f"Variable '{self.name}' value should match regex '{regex}'. Is: {self.value}"


class Attribute:
    __doc__ = 'Models the attribute.'

    def __init__(self, resource, name, value):
        self._resource = resource
        self.name = name
        self.value = value

    @property
    def resource_type(self):
        """Exposes the type of the parent resource object.

        Returns:
            type (basestring): The type of the parent resource

        """
        return self._resource.type

    @property
    def resource_name(self):
        """Exposes the name of the parent resource object.

        Returns:
            name (basestring): The name of the parent resource

        """
        return self._resource.name