# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/schema.py
# Compiled at: 2016-04-12 08:56:16
# Size of source mod 2**32: 2440 bytes
from api_star import renderers
from api_star.compat import getargspec
import coreapi, re, uritemplate

def dedent(content):
    """
    Remove leading indent from a block of text.
    Used when generating descriptions from docstrings.

    Note that python's `textwrap.dedent` doesn't quite cut it,
    as it fails to dedent multiline docstrings that include
    unindented text on the initial line.
    """
    whitespace_counts = [len(line) - len(line.lstrip(' ')) for line in content.splitlines()[1:] if line.lstrip()]
    if whitespace_counts:
        whitespace_pattern = '^' + ' ' * min(whitespace_counts)
        content = re.sub(re.compile(whitespace_pattern, re.MULTILINE), '', content)
    return content.strip()


def get_link(url, method, func):
    """
    Returns a CoreAPI `Link` object for a given view function.
    """
    path_params = uritemplate.variables(url)
    spec = getargspec(func)
    names = spec.args
    num_optional = len(spec.defaults or [])
    num_required = len(names) - num_optional
    required_list = [True for idx in range(num_required)] + [False for idx in range(num_optional)]
    default_location = 'query' if method in ('GET', 'DELETE') else 'form'
    locations = ['path' if name in path_params else default_location for name in names]
    link_description = ''
    field_descriptions = ['' for name in names]
    if func.__doc__:
        docstring = dedent(func.__doc__)
    else:
        docstring = ''
    for line in docstring.splitlines():
        if line.startswith('* '):
            field_name, desc = line.split('-', 1)
            field_descriptions.append(desc.strip())
        else:
            link_description += line + '\n'

    link_description = link_description.strip()
    fields = [coreapi.Field(name=name, required=required, location=location, description=description) for name, required, location, description in zip(names, required_list, locations, field_descriptions)]
    return coreapi.Link(url, action=method, fields=fields, description=link_description)


def add_schema(app, title, url):

    @app.get(url, renderers=[renderers.CoreJSONRenderer()], exclude_from_links=True)
    def schema():
        return coreapi.Document(title=title, url=url, content=app.links)