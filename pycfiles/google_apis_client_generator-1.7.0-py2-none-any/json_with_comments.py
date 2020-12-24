# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/json_with_comments.py
# Compiled at: 2019-01-24 16:56:47
"""Add comments to Json configuration files."""
import json, re, sys
COMMENT_PAT = re.compile('^[ \\t]*#.*$', re.MULTILINE)

def _StripComments(json_string):
    """Strip comments from a json-with-comments string.

  Any line beginning with a pound sign, or with whitespace followed by a pound
  sign, is removed.  Comments are not allowed on the same line as json
  constructs.

  Args:
    json_string: (str) A json string which may contain comments.
  Returns:
    A string without comments.
  """
    return COMMENT_PAT.sub('', json_string)


def Load(fp, **kw):
    """Load json with comments from a file.

  Args:
    fp: (file) A fileish object.
    **kw: (dict) Keyword arguments to pass to the underlying json parser.
  Returns:
    Decoded json data.
  """
    raw = fp.read()
    return Loads(raw, **kw)


def Loads(json_string, **kw):
    """Load json with comments from a string.

  Args:
    json_string: (str|unicode) A string.
    **kw: (dict) Keyword arguments to pass to the underlying json parser.
  Returns:
    Decoded json data.
  """
    stripped = _StripComments(json_string)
    return json.loads(stripped, **kw)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        json_in = open(sys.argv[1])
    else:
        json_in = sys.stdin
    data = Load(json_in)
    json.dump(data, sys.stdout, indent=2)