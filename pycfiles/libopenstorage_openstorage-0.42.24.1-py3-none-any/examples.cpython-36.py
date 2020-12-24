# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/docutils/docutils/examples.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 3959 bytes
"""
This module contains practical examples of Docutils client code.

Importing this module from client code is not recommended; its contents are
subject to change in future Docutils releases.  Instead, it is recommended
that you copy and paste the parts you need into your own code, modifying as
necessary.
"""
from docutils import core, io

def html_parts(input_string, source_path=None, destination_path=None, input_encoding='unicode', doctitle=True, initial_header_level=1):
    """
    Given an input string, returns a dictionary of HTML document parts.

    Dictionary keys are the names of parts, and values are Unicode strings;
    encoding is up to the client.

    Parameters:

    - `input_string`: A multi-line text string; required.
    - `source_path`: Path to the source file or object.  Optional, but useful
      for diagnostic output (system messages).
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `input_encoding`: The encoding of `input_string`.  If it is an encoded
      8-bit string, provide the correct encoding.  If it is a Unicode string,
      use "unicode", the default.
    - `doctitle`: Disable the promotion of a lone top-level section title to
      document title (and subsequent section title to document subtitle
      promotion); enabled by default.
    - `initial_header_level`: The initial level for header elements (e.g. 1
      for "<h1>").
    """
    overrides = {'input_encoding':input_encoding, 
     'doctitle_xform':doctitle, 
     'initial_header_level':initial_header_level}
    parts = core.publish_parts(source=input_string,
      source_path=source_path,
      destination_path=destination_path,
      writer_name='html',
      settings_overrides=overrides)
    return parts


def html_body(input_string, source_path=None, destination_path=None, input_encoding='unicode', output_encoding='unicode', doctitle=True, initial_header_level=1):
    """
    Given an input string, returns an HTML fragment as a string.

    The return value is the contents of the <body> element.

    Parameters (see `html_parts()` for the remainder):

    - `output_encoding`: The desired encoding of the output.  If a Unicode
      string is desired, use the default value of "unicode" .
    """
    parts = html_parts(input_string=input_string,
      source_path=source_path,
      destination_path=destination_path,
      input_encoding=input_encoding,
      doctitle=doctitle,
      initial_header_level=initial_header_level)
    fragment = parts['html_body']
    if output_encoding != 'unicode':
        fragment = fragment.encode(output_encoding)
    return fragment


def internals(input_string, source_path=None, destination_path=None, input_encoding='unicode', settings_overrides=None):
    """
    Return the document tree and publisher, for exploring Docutils internals.

    Parameters: see `html_parts()`.
    """
    if settings_overrides:
        overrides = settings_overrides.copy()
    else:
        overrides = {}
    overrides['input_encoding'] = input_encoding
    output, pub = core.publish_programmatically(source_class=(io.StringInput),
      source=input_string,
      source_path=source_path,
      destination_class=(io.NullOutput),
      destination=None,
      destination_path=destination_path,
      reader=None,
      reader_name='standalone',
      parser=None,
      parser_name='restructuredtext',
      writer=None,
      writer_name='null',
      settings=None,
      settings_spec=None,
      settings_overrides=overrides,
      config_section=None,
      enable_exit_status=None)
    return (pub.writer.document, pub)