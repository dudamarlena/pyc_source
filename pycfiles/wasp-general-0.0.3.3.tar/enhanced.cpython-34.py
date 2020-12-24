# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/command/enhanced.py
# Compiled at: 2017-12-28 02:00:28
# Size of source mod 2**32: 16407 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import re
from abc import abstractmethod
from enum import Enum
from wasp_general.verify import verify_type, verify_value, verify_subclass
from wasp_general.command.command import WCommandProto
from wasp_general.command.proto import WCommandResultProto

class WCommandArgumentParsingError(Exception):
    pass


class WCommandArgumentDescriptor:

    class ArgumentCastingHelperProto:

        @abstractmethod
        @verify_type(argument_name=str)
        @verify_value(argument_name=lambda x: len(x) > 0)
        def cast(self, argument_name, argument_value):
            raise NotImplementedError('This method is abstract')

    class FlagArgumentCastingHelper(ArgumentCastingHelperProto):

        @verify_type(argument_name=str, argument_value=bool)
        @verify_value(argument_name=lambda x: len(x) > 0)
        def cast(self, argument_name, argument_value):
            return argument_value

    class ArgumentCastingHelper(ArgumentCastingHelperProto):

        @verify_type(error_message=(str, None))
        @verify_value(casting_fn=lambda x: x is None or callable(x))
        @verify_value(validate_fn=lambda x: x is None or callable(x))
        def __init__(self, casting_fn=None, validate_fn=None, error_message=None):
            WCommandArgumentDescriptor.ArgumentCastingHelperProto.__init__(self)
            self._ArgumentCastingHelper__casting_fn = casting_fn
            self._ArgumentCastingHelper__validate_fn = validate_fn
            self._ArgumentCastingHelper__error_message = error_message

        def casting_function(self):
            return self._ArgumentCastingHelper__casting_fn

        def validate_function(self):
            return self._ArgumentCastingHelper__validate_fn

        def error_message(self):
            return self._ArgumentCastingHelper__error_message

        @verify_type(argument_name=str, argument_value=str)
        @verify_value(argument_name=lambda x: len(x) > 0)
        def cast(self, argument_name, argument_value):
            casting_fn = self.casting_function()
            if casting_fn is not None:
                argument_value = casting_fn(argument_value)
            validate_fn = self.validate_function()
            if validate_fn is not None:
                if validate_fn(argument_value) is not True:
                    error_message = self.error_message()
                    if error_message is None:
                        error_message = 'Attribute "%s" has invalid value: "%s"' % (
                         argument_name, argument_value)
                    raise WCommandArgumentParsingError(error_message)
            return argument_value

    class StringArgumentCastingHelper(ArgumentCastingHelper):

        @verify_type('paranoid', error_message=(str, None))
        @verify_value('paranoid', validate_fn=lambda x: x is None or callable(x))
        def __init__(self, validate_fn=None, error_message=None):
            WCommandArgumentDescriptor.ArgumentCastingHelper.__init__(self, validate_fn=validate_fn, error_message=error_message)

    class IntegerArgumentCastingHelper(ArgumentCastingHelper):

        @verify_type('paranoid', error_message=(str, None))
        @verify_value('paranoid', validate_fn=lambda x: x is None or callable(x))
        @verify_type(base=int)
        @verify_value(base=lambda x: x > 0)
        def __init__(self, base=10, validate_fn=None, error_message=None):
            WCommandArgumentDescriptor.ArgumentCastingHelper.__init__(self, casting_fn=lambda x: int(x, base=base), validate_fn=validate_fn, error_message=error_message)

    class FloatArgumentCastingHelper(ArgumentCastingHelper):

        @verify_type('paranoid', error_message=(str, None))
        @verify_value('paranoid', validate_fn=lambda x: x is None or callable(x))
        def __init__(self, validate_fn=None, error_message=None):
            WCommandArgumentDescriptor.ArgumentCastingHelper.__init__(self, casting_fn=lambda x: float(x), validate_fn=validate_fn, error_message=error_message)

    class DataSizeArgumentHelper(ArgumentCastingHelper):
        __write_rate_re__ = re.compile('^(\\d+[.\\d]*)([KMGT]?)$')

        def __init__(self):
            WCommandArgumentDescriptor.ArgumentCastingHelper.__init__(self, casting_fn=self.cast_string)

        @staticmethod
        @verify_type(value=str)
        def cast_string(value):
            re_rate = WCommandArgumentDescriptor.DataSizeArgumentHelper.__write_rate_re__.search(value)
            if re_rate is None:
                raise ValueError('Invalid write rate')
            result = float(re_rate.group(1))
            if re_rate.group(2) == 'K':
                result *= 1024
            else:
                if re_rate.group(2) == 'M':
                    result *= 1048576
                else:
                    if re_rate.group(2) == 'G':
                        result *= 1073741824
                    elif re_rate.group(2) == 'T':
                        result *= 1099511627776
            return result

    class EnumArgumentHelper(ArgumentCastingHelper):

        @verify_subclass(enum_cls=Enum)
        def __init__(self, enum_cls):
            WCommandArgumentDescriptor.ArgumentCastingHelper.__init__(self, casting_fn=self.cast_string)
            for item in enum_cls:
                if isinstance(item.value, str) is False:
                    raise TypeError('Enum fields must bt str type')
                    continue

            self._EnumArgumentHelper__enum_cls = enum_cls

        @verify_type(value=str)
        def cast_string(self, value):
            return self._EnumArgumentHelper__enum_cls(value)

    @verify_type(argument_name=str, required=bool, flag_mode=bool, multiple_values=bool, help_info=(str, None))
    @verify_type(meta_var=(str, None), default_value=(str, None))
    @verify_value(argument_name=lambda x: len(x) > 0)
    def __init__(self, argument_name, required=False, flag_mode=False, multiple_values=False, help_info=None, meta_var=None, default_value=None, casting_helper=None):
        """
                note: 'required' is useless for flag-mode attribute
                """
        if flag_mode is True and multiple_values is True or flag_mode is True and default_value is not None or multiple_values is True and default_value is not None:
            raise ValueError('Argument has conflict options. "flag_mode" and "multiple_values" can not be used at the same time')
        if casting_helper is not None:
            flag_helper = WCommandArgumentDescriptor.FlagArgumentCastingHelper
            general_helper = WCommandArgumentDescriptor.ArgumentCastingHelper
            if flag_mode is True and isinstance(casting_helper, flag_helper) is False:
                raise TypeError('casting_helper must be an instance of WCommandArgumentDescriptor.FlagArgumentCastingHelper for flag-mode attribute')
        else:
            if flag_mode is False:
                if isinstance(casting_helper, general_helper) is False:
                    raise TypeError('casting_helper must be an instance of WCommandArgumentDescriptor.ArgumentCastingHelper for every attribute except flag-mode attribute')
            self._WCommandArgumentDescriptor__argument_name = argument_name
            self._WCommandArgumentDescriptor__flag_mode = flag_mode
            self._WCommandArgumentDescriptor__multiple_values = multiple_values
            self._WCommandArgumentDescriptor__default_value = default_value
            self._WCommandArgumentDescriptor__required = required
            self._WCommandArgumentDescriptor__help_info = help_info
            self._WCommandArgumentDescriptor__meta_var = meta_var
        if casting_helper is not None:
            self._WCommandArgumentDescriptor__casting_helper = casting_helper
        else:
            if flag_mode is True:
                self._WCommandArgumentDescriptor__casting_helper = WCommandArgumentDescriptor.FlagArgumentCastingHelper()
            else:
                self._WCommandArgumentDescriptor__casting_helper = WCommandArgumentDescriptor.StringArgumentCastingHelper()

    def argument_name(self):
        return self._WCommandArgumentDescriptor__argument_name

    def flag_mode(self):
        return self._WCommandArgumentDescriptor__flag_mode

    def multiple_values(self):
        return self._WCommandArgumentDescriptor__multiple_values

    def required(self):
        return self._WCommandArgumentDescriptor__required

    def default_value(self):
        return self._WCommandArgumentDescriptor__default_value

    def casting_helper(self):
        return self._WCommandArgumentDescriptor__casting_helper

    @verify_type(argument_name=str)
    @verify_value(argument_name=lambda x: len(x) > 0)
    def cast(self, argument_name, argument_value):
        return self.casting_helper().cast(argument_name, argument_value)

    def help_info(self):
        return self._WCommandArgumentDescriptor__help_info

    def meta_var(self):
        return self._WCommandArgumentDescriptor__meta_var


class WCommandArgumentRelationship:

    class Relationship(Enum):
        conflict = 1
        requirement = 2

    @verify_type(argument_names=str)
    def __init__(self, relationship, *argument_names):
        if isinstance(relationship, WCommandArgumentRelationship.Relationship) is False:
            raise TypeError('Invalid relationship type')
        self._WCommandArgumentRelationship__relationship = relationship
        if len(argument_names) < 2:
            raise ValueError('Relationship can be made with 2 arguments and more')
        self._WCommandArgumentRelationship__arguments = argument_names

    def relationship(self):
        return self._WCommandArgumentRelationship__relationship

    def arguments(self):
        return self._WCommandArgumentRelationship__arguments


class WCommandArgumentParser:

    @verify_type(argument_descriptors=WCommandArgumentDescriptor, relationships=(list, tuple, set, None))
    def __init__(self, *argument_descriptors, relationships=None):
        self._WCommandArgumentParser__descriptors = argument_descriptors
        self._WCommandArgumentParser__relationships = relationships
        if self._WCommandArgumentParser__relationships is not None:
            for relation in self._WCommandArgumentParser__relationships:
                if isinstance(relation, WCommandArgumentRelationship) is False:
                    raise TypeError('Invalid relationship type')
                for argument_name in relation.arguments():
                    argument_found = False
                    for descriptor in self._WCommandArgumentParser__descriptors:
                        if argument_name == descriptor.argument_name():
                            argument_found = True
                            break

                    if argument_found is False:
                        raise ValueError('Relationship with unknown argument was specified')
                        continue

    def descriptors(self):
        return self._WCommandArgumentParser__descriptors

    def relationships(self):
        return self._WCommandArgumentParser__relationships

    def __check_conflict_relation(self, relation, parsed_result):
        argument_found = None
        arguments = relation.arguments()
        for argument_name in arguments:
            if argument_name in parsed_result.keys():
                if argument_found is None:
                    argument_found = argument_name
                else:
                    raise WCommandArgumentParsingError('Conflict arguments was found: %s' % ', '.join(arguments))
                    continue

    def __check_requirements_relation(self, relation, parsed_result):
        arguments = relation.arguments()
        arguments_found = 0
        for argument_name in arguments:
            if argument_name in parsed_result.keys():
                arguments_found += 1
                continue

        if arguments_found > 0:
            if len(arguments) != arguments_found:
                raise WCommandArgumentParsingError("Required arguments wasn't found. The next arguments have mutual requirements: %s" % ', '.join(arguments))

    @verify_type(command_tokens=str)
    def parse(self, *command_tokens):
        descriptors = list(self.descriptors())
        command_tokens = list(command_tokens)
        result = {}
        while len(command_tokens) > 0:
            reduced_command_tokens, descriptors, next_result = self.reduce_tokens(command_tokens.copy(), descriptors.copy(), previous_result=result)
            if len(reduced_command_tokens) >= len(command_tokens):
                raise WCommandArgumentParsingError("Command tokens wasn't reduce")
            command_tokens = reduced_command_tokens
            result = next_result

        relationships = self.relationships()
        if relationships is not None:
            for relation in relationships:
                relation_type = relation.relationship()
                if relation_type == WCommandArgumentRelationship.Relationship.conflict:
                    self._WCommandArgumentParser__check_conflict_relation(relation, result)
                elif relation_type == WCommandArgumentRelationship.Relationship.requirement:
                    self._WCommandArgumentParser__check_requirements_relation(relation, result)
                else:
                    raise RuntimeError('Unknown relationship was specified')

        for descriptor in descriptors:
            argument_name = descriptor.argument_name()
            if descriptor.flag_mode() is True:
                result[argument_name] = descriptor.cast(argument_name, False)
            if descriptor.default_value() is not None:
                result[argument_name] = descriptor.cast(argument_name, descriptor.default_value())
                continue

        for descriptor in self.descriptors():
            if descriptor.required() is True:
                argument_name = descriptor.argument_name()
                if argument_name not in result.keys():
                    raise WCommandArgumentParsingError("Required argument wasn't found: %s" % argument_name)
                else:
                    continue

        return result

    @classmethod
    @verify_type(command_tokens=list, argument_descriptors=list, previous_result=(dict, None))
    def reduce_tokens(cls, command_tokens, argument_descriptors, previous_result=None):
        argument_name = command_tokens.pop(0)
        descriptor = None
        for i in range(len(argument_descriptors)):
            descriptor_to_check = argument_descriptors[i]
            if descriptor_to_check.argument_name() == argument_name:
                descriptor = descriptor_to_check
                if descriptor_to_check.multiple_values() is False:
                    argument_descriptors.pop(i)
                break

        if descriptor is None:
            if argument_name in previous_result.keys():
                raise WCommandArgumentParsingError('Multiple argument ("%s") values found' % argument_name)
            else:
                raise WCommandArgumentParsingError('Unknown argument: "%s"' % argument_name)
        result = previous_result.copy() if previous_result is not None else {}
        if descriptor.flag_mode() is True:
            result[argument_name] = descriptor.cast(argument_name, True)
        else:
            if len(command_tokens) == 0:
                raise WCommandArgumentParsingError("Argument requires value. Value wasn't found")
            argument_value = descriptor.cast(argument_name, command_tokens.pop(0))
            if descriptor.multiple_values() is True:
                if argument_name not in result.keys():
                    result[argument_name] = [
                     argument_value]
                else:
                    result[argument_name].append(argument_value)
            else:
                if argument_name not in result.keys():
                    result[argument_name] = argument_value
                else:
                    raise WCommandArgumentParsingError('Multiple values spotted for the single argument')
        return (
         command_tokens, argument_descriptors, result)

    def arguments_help(self):
        result = []
        for argument in self.descriptors():
            argument_name = argument.argument_name()
            if argument.flag_mode() is not True:
                value_name = argument.meta_var()
                if value_name is None:
                    value_name = 'value'
                argument_name = '%s [%s]' % (argument_name, value_name)
            description = argument.help_info()
            if description is None:
                description = 'argument description unavailable'
            meta = []
            if argument.required() is True:
                meta.append('required')
            if argument.multiple_values() is True:
                meta.append('may have multiple values')
            default_value = argument.default_value()
            if default_value is not None:
                meta.append('default value: %s' % default_value)
            if len(meta) > 0:
                description += ' (%s)' % ', '.join(meta)
            result.append((argument_name, description))

        return tuple(result)


class WEnhancedCommand(WCommandProto):

    @verify_type('paranoid', argument_descriptors=WCommandArgumentDescriptor, relationships=(list, tuple, set, None))
    @verify_type(command=str)
    @verify_value(command=lambda x: len(x) > 0)
    def __init__(self, command, *argument_descriptors, relationships=None):
        WCommandProto.__init__(self)
        self._WEnhancedCommand__command = command
        self._WEnhancedCommand__arguments_descriptors = argument_descriptors
        self._WEnhancedCommand__relationships = relationships
        self._WEnhancedCommand__parser = WCommandArgumentParser(*self.argument_descriptors(), relationships=self.relationships())

    def command_token(self):
        return self._WEnhancedCommand__command

    def argument_descriptors(self):
        return self._WEnhancedCommand__arguments_descriptors

    def relationships(self):
        return self._WEnhancedCommand__relationships

    def parser(self):
        return self._WEnhancedCommand__parser

    @verify_type(command_tokens=str)
    def match(self, *command_tokens, **command_env):
        if len(command_tokens) > 0:
            if command_tokens[0] == self.command_token():
                return True
        return False

    @verify_type(command_tokens=str)
    def exec(self, *command_tokens, **command_env):
        if len(command_tokens) > 0:
            if command_tokens[0] == self.command_token():
                return self._exec(self.parser().parse(*command_tokens[1:]), **command_env)
        raise RuntimeError('Invalid tokens')

    @abstractmethod
    @verify_type(command_arguments=dict)
    def _exec(self, command_arguments, **command_env):
        raise NotImplementedError('This method is abstract')

    def arguments_help(self):
        return self.parser().arguments_help()