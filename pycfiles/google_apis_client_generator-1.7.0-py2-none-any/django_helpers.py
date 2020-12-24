# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/django_helpers.py
# Compiled at: 2019-08-02 14:21:59
"""Wrapper methods to insulate us from Django nuances.

Provide Django setup and some utility methods.
"""
__author__ = 'aiuto@google.com (Tony Aiuto)'
import os
from django import template as django_template
from django import utils as django_utils
from django.conf import settings
try:
    settings.configure()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
except RuntimeError:
    pass

from googleapis.codegen import template_helpers
from googleapis.codegen.filesys import files
_ENGINE = django_template.engine.Engine(builtins=[
 'googleapis.codegen.template_helpers'])

def DjangoRenderTemplate(template_path, context_dict):
    """Renders a template specified by a file path with a give values dict.

  Args:
    template_path: (str) Path to file.
    context_dict: (dict) The dictionary to use for template evaluation.
  Returns:
    (str) The expanded template.
  """
    source = files.GetFileContents(template_path).decode('utf-8')
    return _DjangoRenderTemplateSource(source, context_dict)


def DjangoTemplate(source):
    """Returns a template configured for our default engine.

  Args:
    source: (str) Template source.
  Returns:
    (django.template.Template)
  """
    return django_template.Template(source, engine=_ENGINE)


def _DjangoRenderTemplateSource(template_source, context_dict):
    """Renders the given template source with the given values dict.

  Args:
    template_source: (str) The source of a django template.
    context_dict: (dict) The dictionary to use for template evaluation.
  Returns:
    (str) The expanded template.
  """
    t = DjangoTemplate(template_source)
    ctxt = django_template.Context(context_dict)
    with template_helpers.SetCurrentContext(ctxt):
        return t.render(ctxt)


def MarkSafe(s):
    return django_utils.safestring.mark_safe(s)