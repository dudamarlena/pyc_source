# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/json_expander.py
# Compiled at: 2019-01-24 16:56:47
"""Support for simple JSON templates.

A JSON template is a dictionary of JSON data in which string values
may be simple templates in string.Template format (i.e.,
$dollarSignEscaping).  By default, the template is expanded against
its own data, optionally updated with additional context.
"""
import json
from string import Template
import sys
__author__ = 'smulloni@google.com (Jacob Smullyan)'

def ExpandJsonTemplate(json_data, extra_context=None, use_self=True):
    """Recursively template-expand a json dict against itself or other context.

  The context for string expansion is the json dict itself by default, updated
  by extra_context, if supplied.

  Args:
    json_data: (dict) A JSON object where string values may be templates.
    extra_context: (dict) Additional context for template expansion.
    use_self: (bool) Whether to expand the template against itself, or only use
        extra_context.

  Returns:
    A dict where string template values have been expanded against
    the context.
  """
    if use_self:
        context = dict(json_data)
    else:
        context = {}
    if extra_context:
        context.update(extra_context)

    def RecursiveExpand(obj):
        if isinstance(obj, list):
            return [ RecursiveExpand(x) for x in obj ]
        else:
            if isinstance(obj, dict):
                return dict((k, RecursiveExpand(v)) for k, v in obj.iteritems())
            if isinstance(obj, (str, unicode)):
                return Template(obj).safe_substitute(context)
            return obj

    return RecursiveExpand(json_data)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        json_in = open(sys.argv[1])
    else:
        json_in = sys.stdin
    data = json.load(json_in)
    expanded = ExpandJsonTemplate(data)
    json.dump(expanded, sys.stdout, indent=2)