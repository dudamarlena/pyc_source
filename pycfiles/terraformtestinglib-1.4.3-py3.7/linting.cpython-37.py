# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/terraformtestinglib/terraformtestinglib/linting/linting.py
# Compiled at: 2019-10-22 09:46:12
# Size of source mod 2**32: 18381 bytes
"""
Main code for linting.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging, os, re, warnings, yaml
from yaml.parser import ParserError
from schema import SchemaError
from terraformtestinglib.terraformtestinglib import Parser
from terraformtestinglib.configuration import NAMING_SCHEMA, POSITIONING_SCHEMA, DISASTER_RECOVERY_FILENAME
from terraformtestinglib.terraformtestinglibexceptions import InvalidNaming, InvalidPositioning
from terraformtestinglib.utils import RuleError, ResourceError, FilenameError, ConfigurationError
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'linting'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class Stack(Parser):
    __doc__ = 'Manages a stack as a collection of resources that can be checked for name convention.'

    def __init__(self, configuration_path, naming_file_path, positioning_file_path=None, global_variables_file_path=None, file_to_skip_for_positioning=None, raise_on_missing_variable=True, environment_variables=None):
        super(Stack, self).__init__(configuration_path, global_variables_file_path, raise_on_missing_variable, environment_variables)
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.path = configuration_path
        self.rules_set = self._get_naming_rules(naming_file_path)
        self.positioning = self._get_positioning_rules(positioning_file_path)
        self.positioning_skip_file = file_to_skip_for_positioning
        self.resources = self._get_resources()
        self._errors = []

    @staticmethod
    def _get_naming_rules(rules_file):
        try:
            rules_path_file = os.path.expanduser(rules_file)
            with open(rules_path_file, 'r') as (rules_file_handle):
                rules = yaml.load((rules_file_handle.read()), Loader=(yaml.FullLoader))
                rules_file_handle.close()
            rules = NAMING_SCHEMA.validate(rules)
        except IOError:
            raise InvalidNaming('Could not load naming file')
        except ParserError:
            raise InvalidNaming('Unable to parse yaml file. Please check that it is valid.')
        except SchemaError as error:
            try:
                raise InvalidNaming(error)
            finally:
                error = None
                del error

        return RuleSet(rules)

    @staticmethod
    def _get_positioning_rules(positioning_file):
        if positioning_file is None:
            return
        try:
            positioning_path_file = os.path.expanduser(positioning_file)
            with open(positioning_path_file, 'r') as (positioning_file_handle):
                positioning = yaml.load((positioning_file_handle.read()), Loader=(yaml.FullLoader))
                positioning_file_handle.close()
            positioning = POSITIONING_SCHEMA.validate(positioning)
        except IOError:
            raise InvalidPositioning('Could not load positioning file')
        except ParserError:
            raise InvalidPositioning('Unable to parse yaml file. Please check that it is valid.')
        except SchemaError as error:
            try:
                raise InvalidPositioning(error)
            finally:
                error = None
                del error

        return positioning

    def _get_resources(self):
        resources = []
        for hcl_resource in self.hcl_resources:
            if hcl_resource.data.get('count'):
                for data in self.hcl_view.get_counter_resource_data_by_type(hcl_resource.resource_type, hcl_resource.resource_name):
                    resources.append(self._instantiate_resource(hcl_resource.filename, hcl_resource.resource_type, hcl_resource.resource_name, data, hcl_resource.data))

            else:
                resources.append(self._instantiate_resource(hcl_resource.filename, hcl_resource.resource_type, hcl_resource.resource_name, self.hcl_view.get_resource_data_by_type(hcl_resource.resource_type, hcl_resource.resource_name), hcl_resource.data))

        return resources

    def _instantiate_resource(self, filename, resource_type, name, data, original_data):
        resource = LintingResource(filename, resource_type, name, data, original_data)
        resource.register_rules_set(self.rules_set)
        if filename == self.positioning_skip_file:
            resource.register_positioning_set(None)
        else:
            resource.register_positioning_set(self.positioning)
        return resource

    def validate(self):
        """Validates all the resources of the stack.

        Returns:
            None

        """
        self._errors = []
        for resource in self.resources:
            resource.validate()
            for error in resource.errors:
                self._errors.append(error)

    @property
    def errors(self):
        """The errors of the validation of the resources of the stack.

        Returns:
            errors (ResourceError|FilenameError) : list of possible linting errors

        """
        return self._errors


class LintingResource:
    __doc__ = 'Manages a resource and provides validation capabilities..'

    def __init__(self, filename, resource_type, name, data, original_data):
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.filename = filename
        self.name = name
        self.type = resource_type
        self.data = data
        self.original_data = original_data
        self.rules_set = None
        self.positioning_set = None
        self.errors = None

    def __getattr__(self, value):
        return self.data.get(value)

    def register_rules_set(self, rules_set):
        """Registers the set of rules with the Resource.

        Args:
            rules_set (dict): A dictionary with the rules for the naming convention

        Returns:
            None

        """
        self.rules_set = rules_set

    def register_positioning_set(self, positioning_set):
        """Registers the set of rules with the Resource.

        Args:
            positioning_set (dict): A dictionary with the rules for the positioning convention

        Returns:
            None

        """
        self.positioning_set = positioning_set

    def _get_entity_desired_filename(self, entity):
        target = next((filename for filename, entities in self.positioning_set.items() if entity in entities), 'unknown')
        return target

    def validate(self):
        """Validates the resource according to the appropriate rule.

        Returns:
            True upon completion

        """
        self.errors = []
        validate_positioning = True
        if not self.rules_set:
            self._logger.warning('No rules set!')
            return True
        elif self.positioning_set is None:
            message = 'Skipping resource positioning due to positioning file not been provided or being skipped.'
            self._logger.info(message)
            validate_positioning = False
        else:
            if os.environ.get('SKIP_POSITIONING'):
                self._logger.info('Skipping resource positioning due to global environment setting.')
                validate_positioning = False
        self._logger.debug('Resource type %s', self.type)
        self._validate_naming()
        if self.filename == DISASTER_RECOVERY_FILENAME:
            self._logger.info('Not validating entries for "%s"', DISASTER_RECOVERY_FILENAME)
            return True
        if validate_positioning:
            self._validate_positioning()
        return True

    def _is_check_skipped(self, tag_name, deprecated_tag_name=None):
        skip_check = False
        try:
            check_tag = tag_name
            deprecated_tag = deprecated_tag_name
            tags = self.tags or {}
            if tags.get(deprecated_tag):
                message = f'The tag "{deprecated_tag}" is deprecated. Please use "{check_tag}". Resource: {self.name}'
                warnings.warn(message, PendingDeprecationWarning)
                check_tag = deprecated_tag
            skip_check = tags.get(check_tag, False)
        except IndexError:
            self._logger.error((
             'Weird error with no or broken resources found %s for resource %s' % self.data, self.name))
        except AttributeError:
            self._logger.exception('Multiple tags entry found on resource %s', self.name)

        return skip_check

    def _validate_positioning(self):
        self._logger.debug('Resource name %s', self.name)
        if self._is_check_skipped('skip-positioning', 'skip_positioning'):
            self._logger.warning('Skipping resource %s positioning checking due to user overriding tag.', self.name)
        else:
            full_desired_filename = self._get_entity_desired_filename(self.type)
            desired_filename, _, _ = full_desired_filename.rpartition('.tf')
            file_name, _, _ = self.filename.rpartition('.')
            if not re.match(desired_filename, file_name):
                self.errors.append(FilenameError(self.filename, self.name, full_desired_filename))
                self._logger.error('Filename positioning not followed on file %s for resource %s. Should be in a file matching %s.tf .', self.filename, self.name, desired_filename)
        return True

    def _validate_naming(self):
        self._logger.debug('Resource name %s', self.name)
        if self._is_check_skipped('skip-linting', 'skip_linting'):
            self._logger.warning('Skipping resource %s naming checking due to user overriding tag.', self.name)
        else:
            rule = self.rules_set.get_rule_for_resource(self.type)
            if rule:
                self._logger.debug('Found matching rule "%s"', rule.regex)
                rule.validate(self.type, self.name, self.data, self.original_data)
                for error in rule.errors:
                    if isinstance(error, ConfigurationError):
                        self._logger.error('Invalid configuration found on file %s for resource %s with type %s . Invalid value found :%s', self.filename, error.entity, error.field, error.value)
                    else:
                        self._logger.error('Naming convention not followed on file %s for resource %s with type %s. Regex not matched :%s. Value :%s', self.filename, error.entity, error.field, error.regex, error.value)
                    self.errors.append(ResourceError(self.filename, *error))

            else:
                self._logger.debug('No matching rule found')
        return True


class RuleSet:
    __doc__ = 'Manages the rules as a group and can search them by name.'

    def __init__(self, rules):
        self._rules = rules

    def get_rule_for_resource(self, resource_name):
        """Retrieves the rule for the resource name.

        Args:
            resource_name (basestring): The resource type to retrieve the rule for

        Returns:
            The rule corresponding with the resource type if found, None otherwise

        """
        return next((Rule(rule) for rule in self._rules if rule.get('resource') == resource_name), None)


class Rule:
    __doc__ = 'Handles the rule object providing validation capabilities.'

    def __init__(self, data):
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.data = data
        self.regex = self.data.get('regex')
        self._errors = []

    @property
    def errors(self):
        """List of errors found.

        Returns: The errors found

        """
        return self._errors

    @errors.setter
    def errors(self, error):
        self._errors.append(error)

    def validate(self, resource_type, resource_name, resource_data, original_data):
        """Validates the given resource based on the ruleset.

        Args:
            resource_type (basestring): The type of the resource
            resource_name (basestring): The name of the resource
            resource_data (dict): The interpolated data of the resource
            original_data (dict): The original data of the resource, before the interpolation

        Returns:
            True on successful validation, False otherwise

        """
        if not self.regex:
            return True
        else:
            self._validate_name(resource_type, resource_name)
            self._validate_values(resource_type, resource_name, resource_data, original_data)
            return self.errors or True
        return False

    def _validate_name(self, resource_type, resource_name):
        rule = re.compile(self.regex)
        if not re.match(rule, resource_name):
            self.errors = RuleError(resource_type, resource_name, 'id', self.regex, resource_name, None)

    def _validate_values(self, resource_type, resource_name, resource_data, original_data):
        for field in self.data.get('fields', []):
            regex = field.get('regex')
            if not regex:
                continue
            rule = re.compile(regex)
            original_value, key_name = self._get_value_from_resource(original_data, field.get('value'))
            value, key_name = self._get_value_from_resource(resource_data, field.get('value'))
            original_value = original_value if original_value != value else None
            rule_arguments = [resource_type, resource_name, field.get('value'), regex, value, original_value]
            if isinstance(value, list):
                for entry in value:
                    rule_arguments[4] = entry.get(key_name)
                    self._match_rule_to_value(regex, rule, entry.get(key_name), rule_arguments)

            else:
                self._match_rule_to_value(regex, rule, value, rule_arguments)

    def _match_rule_to_value(self, regex, rule, value, rule_arguments):
        try:
            if not re.match(rule, value):
                self.errors = RuleError(*rule_arguments)
        except TypeError:
            self._logger.error('Error matching for regex, values passed were, rule:%s value:%s', regex, value)

    def _get_value_from_resource(self, resource, value):
        path = value.split('.')
        for entry in path:
            try:
                field = resource.get(entry)
            except AttributeError:
                self._logger.error('Error getting field %s, failed for path %s', value, path)

            resource = field
            if isinstance(resource, list):
                keys_path = value.split('.')
                return (resource, keys_path.pop(keys_path.index(entry) + 1))

        return (
         resource, None)