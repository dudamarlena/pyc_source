# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/util.py
# Compiled at: 2019-04-23 17:42:56
# Size of source mod 2**32: 2302 bytes
__doc__ = '\nurl builder related utility methods.\n'
from six import PY2
from requests.compat import urlparse
from requests.models import PreparedRequest

def get_netloc(url):
    """
    Get network location part of an url.

    For example: https://www.python.org/doc/ -> www.python.org
    """
    parse_result = urlparse(url)
    netloc = parse_result.netloc
    return netloc


def get_domain(url, ensure_http=True):
    """
    Get domain part of an url.

    For example: https://www.python.org/doc/ -> https://www.python.org
    """
    if ensure_http:
        if not (url.startswith('https') or url.startswith('http')):
            raise ValueError('%s not start with `http` or `https`!' % url)
    parse_result = urlparse(url)
    domain = '{schema}://{netloc}'.format(schema=(parse_result.scheme),
      netloc=(parse_result.netloc))
    return domain


def join_all(domain, *parts):
    """
    Join all url components.

    :rtype: str
    :param domain: Domain parts, example: https://www.python.org

    :rtype: list
    :param parts: Other parts, example: "/doc", "/py27"

    :rtype: str
    :return: url

    Example::

        >>> join_all("https://www.apple.com", "iphone")
        https://www.apple.com/iphone
    """
    l = list()
    if domain.endswith('/'):
        domain = domain[:-1]
    l.append(domain)
    for part in parts:
        for i in part.split('/'):
            if i.strip():
                l.append(i)

    url = '/'.join(l)
    return url


def add_params(endpoint, params):
    """
    Combine query endpoint and params.

    :type endpoint: str
    :param endpoint:

    :type params: list, tuple, dict
    :param params:

    Example::

        >>> add_params("https://www.google.com/search", {"q": "iphone"})
        https://www.google.com/search?q=iphone
    """
    p = PreparedRequest()
    p.prepare(url=endpoint, params=params)
    if PY2:
        return unicode(p.url)
    else:
        return p.url


def get_all_subclass(klass):
    """
    Get all subclass. Return a set.

    :rtype: set
    :return:
    """
    subclasses = set()
    for subklass in klass.__subclasses__():
        subclasses.add(subklass)
        subclasses.update(get_all_subclass(subklass))

    return subclasses