# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/cli/types.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 7708 bytes
"""
Implementation of custom click parameter types
"""
import re, json
from json import JSONDecodeError
import click
PARAM_AND_METADATA_KEY_REGEX = '([A-Za-z0-9\\"]+)'

def _generate_match_regex(match_pattern, delim):
    """
    Creates a regex string based on a match pattern (also a regex) that is to be
    run on a string (which may contain escaped quotes) that is separated by delimiters.

    Parameters
    ----------
    match_pattern: (str) regex pattern to match
    delim: (str) delimiter that is respected when identifying matching groups with generated regex.

    Returns
    -------
    str: regex expression

    """
    return f'(\\"(?:\\\\{match_pattern}|[^\\"\\\\]+)*\\"|(?:\\\\{match_pattern}|[^{delim}\\"\\\\]+)+)'


def _unquote_wrapped_quotes(value):
    r"""
    Removes wrapping double quotes and any '\ ' characters. They are usually added to preserve spaces when passing
    value thru shell.

    Examples
    --------
    >>> _unquote_wrapped_quotes('val\ ue')
    value

    >>> _unquote_wrapped_quotes("hel\ lo")
    hello

    Parameters
    ----------
    value : str
        Input to unquote

    Returns
    -------
    Unquoted string
    """
    if value:
        if value[0] == value[(-1)] == '"':
            value = value.strip('"')
    return value.replace('\\ ', ' ').replace('\\"', '"')


class CfnParameterOverridesType(click.ParamType):
    __doc__ = '\n    Custom Click options type to accept values for CloudFormation template parameters. You can pass values for\n    parameters as "ParameterKey=KeyPairName,ParameterValue=MyKey ParameterKey=InstanceType,ParameterValue=t1.micro"\n    '
    _CfnParameterOverridesType__EXAMPLE_1 = 'ParameterKey=KeyPairName,ParameterValue=MyKey ParameterKey=InstanceType,ParameterValue=t1.micro'
    _CfnParameterOverridesType__EXAMPLE_2 = 'KeyPairName=MyKey InstanceType=t1.micro'
    VALUE_REGEX_SPACE_DELIM = _generate_match_regex(match_pattern='.', delim=' ')
    _pattern_1 = '(?:ParameterKey={key},ParameterValue={value})'.format(key=PARAM_AND_METADATA_KEY_REGEX,
      value=VALUE_REGEX_SPACE_DELIM)
    _pattern_2 = '(?:(?: ){key}={value})'.format(key=PARAM_AND_METADATA_KEY_REGEX, value=VALUE_REGEX_SPACE_DELIM)
    ordered_pattern_match = [
     _pattern_1, _pattern_2]
    name = ''

    def convert(self, value, param, ctx):
        result = {}
        if value == ('', ):
            return result
        value = (value,) if isinstance(value, str) else value
        for val in value:
            val.strip()
            val = ' ' + val
            try:
                pattern = next((i for i in filter(lambda item: re.findall(item, val), self.ordered_pattern_match)))
            except StopIteration:
                return self.fail("{} is not in valid format. It must look something like '{}' or '{}'".format(val, self._CfnParameterOverridesType__EXAMPLE_1, self._CfnParameterOverridesType__EXAMPLE_2), param, ctx)
            else:
                groups = re.findall(pattern, val)
                for key, param_value in groups:
                    result[_unquote_wrapped_quotes(key)] = _unquote_wrapped_quotes(param_value)

        return result


class CfnMetadataType(click.ParamType):
    __doc__ = '\n    Custom Click options type to accept values for metadata parameters.\n    metadata parameters can be of the type KeyName1=string,KeyName2=string or {"string":"string"}\n    '
    _EXAMPLE = 'KeyName1=string,KeyName2=string or {"string":"string"}'
    VALUE_REGEX_COMMA_DELIM = _generate_match_regex(match_pattern='.', delim=',')
    _pattern = '(?:{key}={value})'.format(key=PARAM_AND_METADATA_KEY_REGEX, value=VALUE_REGEX_COMMA_DELIM)
    name = ''

    def convert(self, value, param, ctx):
        result = {}
        fail = False
        if not value:
            return result
        try:
            result = json.loads(value)
            for val in result.values():
                if isinstance(val, (dict, list)):
                    fail = True

        except JSONDecodeError:
            groups = re.findall(self._pattern, value)
            if not groups:
                fail = True
            for group in groups:
                key, v = group
                result[key] = v

        if fail:
            return self.fail("{} is not in valid format. It must look something like '{}'".format(value, self._EXAMPLE), param, ctx)
        return result


class CfnTags(click.ParamType):
    __doc__ = '\n    Custom Click options type to accept values for tag parameters.\n    tag parameters can be of the type KeyName1=string KeyName2=string\n    '
    _EXAMPLE = 'KeyName1=string KeyName2=string'
    TAG_REGEX = '[A-Za-z0-9\\"_:\\.\\/\\+-\\@=]'
    _pattern = '{tag}={tag}'.format(tag=_generate_match_regex(match_pattern=TAG_REGEX, delim=' '))
    name = ''

    def convert(self, value, param, ctx):
        result = {}
        fail = False
        if value == ('', ):
            return result
        value = (value,) if not isinstance(value, tuple) else value
        for val in value:
            groups = re.findall(self._pattern, val)
            if not groups:
                fail = True
            for group in groups:
                key, v = group
                result[_unquote_wrapped_quotes(key)] = _unquote_wrapped_quotes(v)

            if fail:
                return self.fail("{} is not in valid format. It must look something like '{}'".format(value, self._EXAMPLE), param, ctx)

        return result