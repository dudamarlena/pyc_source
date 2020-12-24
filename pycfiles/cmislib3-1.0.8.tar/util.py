# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/util.py
# Compiled at: 2016-12-29 16:45:15
__doc__ = '\nThis module contains handy utility functions.\n'
import re, iso8601, logging, datetime
from cmislib.domain import CmisId
from urllib import urlencode, quote
moduleLogger = logging.getLogger('cmislib.util')

def to_utf8(value):
    """ Safe encodng of value to utf-8 taking care of unicode values
    """
    if isinstance(value, unicode):
        value = value.encode('utf8')
    return value


def safe_urlencode(in_dict):
    """
    Safe encoding of values taking care of unicode values
    urllib.urlencode doesn't like unicode values
    """

    def encoded_dict(in_dict):
        out_dict = {}
        for k, v in in_dict.iteritems():
            out_dict[k] = to_utf8(v)

        return out_dict

    return urlencode(encoded_dict(in_dict))


def safe_quote(value):
    """
    Safe encoding of value taking care of unicode value
    urllib.quote doesn't like unicode values
    """
    return quote(to_utf8(value))


def multiple_replace(aDict, text):
    """
    Replace in 'text' all occurences of any key in the given
    dictionary by its corresponding value.  Returns the new string.

    See http://code.activestate.com/recipes/81330/
    """
    regex = re.compile('(%s)' % ('|').join(map(re.escape, aDict.keys())))
    return regex.sub(lambda mo: aDict[mo.string[mo.start():mo.end()]], text)


def parsePropValue(value, nodeName):
    """
    Returns a properly-typed object based on the type as specified in the
    node's element name.
    """
    moduleLogger.debug('Inside parsePropValue')
    if nodeName == 'propertyId':
        return CmisId(value)
    else:
        if nodeName == 'propertyString':
            return value
        if nodeName == 'propertyBoolean':
            bDict = {'false': False, 'true': True}
            return bDict[value.lower()]
        if nodeName == 'propertyInteger':
            return int(value)
        if nodeName == 'propertyDecimal':
            return float(value)
        if nodeName == 'propertyDateTime':
            return parseDateTimeValue(value)
        return value


def parsePropValueByType(value, typeName):
    """
    Returns a properly-typed object based on the type as specified in the
    node's property definition.
    """
    moduleLogger.debug('Inside parsePropValueByType: %s: %s', typeName, value)
    if typeName == 'id':
        if value:
            return CmisId(value)
        else:
            return

    else:
        if typeName == 'string':
            return value
        if typeName == 'boolean':
            if not value:
                return False
            else:
                if type(value) == bool:
                    return value
                bDict = {'false': False, 'true': True}
                return bDict[value.lower()]

        elif typeName == 'integer':
            if value:
                return int(value)
            else:
                return 0

        elif typeName == 'decimal':
            if value:
                if isinstance(value, list):
                    return float(value[0])
                else:
                    return float(value)

            else:
                return 0.0
        else:
            if typeName == 'datetime':
                return parseDateTimeValue(value)
            else:
                return value

    return


def parseDateTimeValue(value):
    """
    Utility function to return a datetime from a string.
    """
    if type(value) == str or type(value) == unicode:
        return iso8601.parse_date(value)
    else:
        if type(value) == int:
            return datetime.datetime.fromtimestamp(value / 1000)
        moduleLogger.debug('Could not parse dt value of type: %s' % type(value))
        return


def parseBoolValue(value):
    """
    Utility function to parse booleans and none from strings
    """
    if value == 'false':
        return False
    else:
        if value == 'true':
            return True
        else:
            if value == 'none':
                return
            return value

        return


def toCMISValue(value):
    """
    Utility function to convert Python values to CMIS string values
    """
    if value is False:
        return 'false'
    else:
        if value is True:
            return 'true'
        else:
            if value is None:
                return 'none'
            return value

        return