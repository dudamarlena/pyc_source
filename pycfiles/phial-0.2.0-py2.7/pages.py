# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/phial/pages.py
# Compiled at: 2014-04-22 23:03:09
__all__ = [
 'register_page', 'register_assets', 'register_simple_assets',
 'page', 'RenderedPage', 'ResolvedAsset']
from . import exceptions
from . import documents
from . import utils
import logging
log = logging.getLogger(__name__)
_pages = []
_assets = []

def register_page(func, *args, **kwargs):
    _pages.append(Page(func, *args, **kwargs))
    log.debug('Collected page with function %r from module %r.', func.__name__, func.__module__)


def register_assets(target, *files):
    _assets.append(Asset(target, files))


def register_simple_assets(*files):
    register_assets(None, *files)
    return


def page(*dec_args, **dec_kwargs):

    def real_decorator(function):
        register_page(function, *dec_args, **dec_kwargs)
        return function

    return real_decorator


class RenderedPage(object):
    """
    Represents a single page (rather than a type of page like pages.Page
    objects). The page can be an HTML file, a CSS stylesheet, a cat picture,
    or even a blank file.

    :ivar target: The path (relative to the output directory) that the content
            should be written into.
    :ivar content: The page's content. Can either be a ``unicode`` object (in
            which case it will be written to the target file using the
            configured output encoding) or a ``str`` object (it will be
            written directly to the file).

    """

    def __init__(self, target, content):
        self.target = target
        self.content = content


class ResolvedAsset(object):
    """
    Represents a single static page. Static in this case means that no
    processing has to be done on the contents of the source file.

    :ivar target: The path (relative to the output directory) that the source
            should be copied to.
    :ivar source: The path (relative to the source directory) of the file to
            be copied.
    """

    def __init__(self, target, source):
        self.target = target
        self.source = source

    def __repr__(self):
        return ('ResolvedAsset(target = {!r}, source = {!r})').format(self.target, self.source)


class Asset(object):
    """
    Conceptually represents a glob of static pages. Static in this case means
    that no processing has to be done on the contents of the source file(s).

    :ivar target: The path (relative to the output directory) that the source
            file will be copied to. Similarly to Path.target,  this string will
            be run through `str.format() <http://docs.python.org/2/library/stdtypes.html#str.format>`_
            for each file.
    :ivar files: May be a string, or a list of strings.  If a string, that string will be globbed, if a list of strings, each string in the list will be globbed. All matching files will be copied to the target.

    """

    def __init__(self, target, files):
        self.target = target
        self.files = files


class Page(object):
    """
    Conceptually represents a type of page on a site (ex: a project page, the
    home page, or a blog post). Pages always have a function associated with
    them that produces the actual content.

    :ivar func: The function that will be called to generate the page.
    :ivar target: The desired relative target of the page. This string will be
            run through `str.format() <http://docs.python.org/2/library/stdtypes.html#str.format>`_
            for each file. If ``None``, a ``RenderedPage`` object must be
            returned by ``func`` that specifies an explicit ``target``.
    :ivar files: May be ``None``, a string, or a list of strings.  If a
            string, that string will be globbed and ``func`` will be called
            for each unique matching file. If a list of strings, each
            string in the list will be globbed and then ``func`` will be
            called for each unique matching file. If ``None``, ``func``
            will be called only once.
    :ivar parse_files: If True each file will be opened and a Document
            object will be given to your function. Any frontmatter in the
            file will be parsed out. If False, your function will only
            receive the path of the matched file.

    """

    def __init__(self, func, target=None, files=None, parse_files=True):
        self.func = func
        self.target = target
        self.files = files
        self.parse_files = parse_files

    def __repr__(self):
        return ('Page(func = {!r}, target = {!r}, files = {!r}, parse_files = {!r}').format(self.func, self.target, self.files, self.parse_files)