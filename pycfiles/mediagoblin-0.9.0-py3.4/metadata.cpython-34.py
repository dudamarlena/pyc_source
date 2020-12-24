# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/metadata.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 6601 bytes
from io import open
import os, copy, json, re
from pkg_resources import resource_filename
import dateutil.parser
from pyld import jsonld
from jsonschema import validate, FormatChecker, draft4_format_checker
from jsonschema.compat import str_types
from mediagoblin.tools.pluginapi import hook_handle
URL_REGEX = re.compile('^[a-z]+://([^/:]+|([0-9]{1,3}\\.){3}[0-9]{1,3})(:[0-9]+)?(\\/.*)?$', re.IGNORECASE)

def is_uri(instance):
    """
    jsonschema uri validator
    """
    if not isinstance(instance, str_types):
        return True
    return URL_REGEX.match(instance)


def is_datetime(instance):
    """
    Is a date or datetime readable string.
    """
    if not isinstance(instance, str_types):
        return True
    return dateutil.parser.parse(instance)


class DefaultChecker(FormatChecker):
    __doc__ = '\n    Default MediaGoblin format checker... extended to include a few extra things\n    '
    checkers = copy.deepcopy(draft4_format_checker.checkers)


DefaultChecker.checkers['uri'] = (
 is_uri, ())
DefaultChecker.checkers['date-time'] = (is_datetime, (ValueError, TypeError))
DEFAULT_CHECKER = DefaultChecker()
DEFAULT_SCHEMA = {'$schema': 'http://json-schema.org/schema#', 
 'type': 'object', 
 'properties': {'license': {'format': 'uri', 
                            'type': 'string'}, 
                'dcterms:created': {'format': 'date-time', 
                                    'type': 'string'}, 
                'dc:created': {'format': 'date-time', 
                               'type': 'string'}}}

def load_resource(package, resource_path):
    """
    Load a resource, return it as a string.

    Args:
    - package: package or module name.  Eg "mediagoblin.media_types.audio"
    - resource_path: path to get to this resource, a list of
      directories and finally a filename.  Will be joined with
      os.path.sep.
    """
    filename = resource_filename(package, os.path.sep.join(resource_path))
    return open(filename, encoding='utf-8').read()


def load_resource_json(package, resource_path):
    """
    Load a resource json file, return a dictionary.

    Args:
    - package: package or module name.  Eg "mediagoblin.media_types.audio"
    - resource_path: path to get to this resource, a list of
      directories and finally a filename.  Will be joined with
      os.path.sep.
    """
    return json.loads(load_resource(package, resource_path))


BUILTIN_CONTEXTS = {'http://www.w3.org/2013/json-ld-context/rdfa11': load_resource('mediagoblin', ['static', 'metadata', 'rdfa11.jsonld'])}
_CONTEXT_CACHE = {}

def load_context(url):
    """
    A self-aware document loader.  For those contexts MediaGoblin
    stores internally, load them from disk.
    """
    if url in _CONTEXT_CACHE:
        return _CONTEXT_CACHE[url]
    document = BUILTIN_CONTEXTS.get(url, None)
    if document is None:
        document = hook_handle(('context_url_data', url))
    if document is not None:
        document = {'contextUrl': None,  'documentUrl': url,  'document': document}
    else:
        document = jsonld.load_document(url)
    _CONTEXT_CACHE[url] = document
    return document


DEFAULT_CONTEXT = 'http://www.w3.org/2013/json-ld-context/rdfa11'

def compact_json(metadata, context=DEFAULT_CONTEXT):
    """
    Compact json with supplied context.

    Note: Free floating" nodes are removed (eg a key just named
    "bazzzzzz" which isn't specified in the context... something like
    bazzzzzz:blerp will stay though.  This is jsonld.compact behavior.
    """
    compacted = jsonld.compact(metadata, context, options={'documentLoader': load_context, 
     'expandContext': context, 
     'keepFreeFloatingNodes': False})
    return compacted


def compact_and_validate(metadata, context=DEFAULT_CONTEXT, schema=DEFAULT_SCHEMA):
    """
    compact json with supplied context, check against schema for errors

    raises an exception (jsonschema.exceptions.ValidationError) if
    there's an error.

    Note: Free floating" nodes are removed (eg a key just named
    "bazzzzzz" which isn't specified in the context... something like
    bazzzzzz:blerp will stay though.  This is jsonld.compact behavior.

    You may wish to do this validation yourself... this is just for convenience.
    """
    compacted = compact_json(metadata, context)
    validate(metadata, schema, format_checker=DEFAULT_CHECKER)
    return compacted


def expand_json(metadata, context=DEFAULT_CONTEXT):
    """
    Expand json, but be sure to use our documentLoader.

    By default this expands with DEFAULT_CONTEXT, but if you do not need this,
    you can safely set this to None.

    # @@: Is the above a good idea?  Maybe it should be set to None by
    #   default.
    """
    options = {'documentLoader': load_context}
    if context is not None:
        options['expandContext'] = context
    return jsonld.expand(metadata, options=options)


def rdfa_to_readable(rdfa_predicate):
    readable = rdfa_predicate.split(':')[1].capitalize()
    return readable