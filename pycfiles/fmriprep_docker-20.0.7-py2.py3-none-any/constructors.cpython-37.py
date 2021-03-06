# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/req/constructors.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 15441 bytes
"""Backing implementation for InstallRequirement's various constructors

The idea here is that these formed a major chunk of InstallRequirement's size
so, moving them and support code dedicated to them outside of that class
helps creates for better understandability for the rest of the code.

These are meant to be used elsewhere within pip to create instances of
InstallRequirement.
"""
import logging, os, re
from pip._vendor.packaging.markers import Marker
from pip._vendor.packaging.requirements import InvalidRequirement, Requirement
from pip._vendor.packaging.specifiers import Specifier
from pip._vendor.pkg_resources import RequirementParseError, parse_requirements
from pip._internal.exceptions import InstallationError
from pip._internal.models.index import PyPI, TestPyPI
from pip._internal.models.link import Link
from pip._internal.models.wheel import Wheel
from pip._internal.pyproject import make_pyproject_path
from pip._internal.req.req_install import InstallRequirement
from pip._internal.utils.filetypes import ARCHIVE_EXTENSIONS
from pip._internal.utils.misc import is_installable_dir, splitext
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.urls import path_to_url
from pip._internal.vcs import is_url, vcs
if MYPY_CHECK_RUNNING:
    from typing import Any, Dict, Optional, Set, Tuple, Union
    from pip._internal.req.req_file import ParsedRequirement
__all__ = [
 'install_req_from_editable', 'install_req_from_line',
 'parse_editable']
logger = logging.getLogger(__name__)
operators = Specifier._operators.keys()

def is_archive_file(name):
    """Return True if `name` is a considered as an archive file."""
    ext = splitext(name)[1].lower()
    if ext in ARCHIVE_EXTENSIONS:
        return True
    return False


def _strip_extras(path):
    m = re.match('^(.+)(\\[[^\\]]+\\])$', path)
    extras = None
    if m:
        path_no_extras = m.group(1)
        extras = m.group(2)
    else:
        path_no_extras = path
    return (path_no_extras, extras)


def convert_extras(extras):
    if not extras:
        return set()
    return Requirement('placeholder' + extras.lower()).extras


def parse_editable(editable_req):
    """Parses an editable requirement into:
        - a requirement name
        - an URL
        - extras
        - editable options
    Accepted requirements:
        svn+http://blahblah@rev#egg=Foobar[baz]&subdirectory=version_subdir
        .[some_extra]
    """
    url = editable_req
    url_no_extras, extras = _strip_extras(url)
    if os.path.isdir(url_no_extras):
        if not os.path.exists(os.path.join(url_no_extras, 'setup.py')):
            msg = 'File "setup.py" not found. Directory cannot be installed in editable mode: {}'.format(os.path.abspath(url_no_extras))
            pyproject_path = make_pyproject_path(url_no_extras)
            if os.path.isfile(pyproject_path):
                msg += '\n(A "pyproject.toml" file was found, but editable mode currently requires a setup.py based build.)'
            raise InstallationError(msg)
        url_no_extras = path_to_url(url_no_extras)
    if url_no_extras.lower().startswith('file:'):
        package_name = Link(url_no_extras).egg_fragment
        if extras:
            return (package_name,
             url_no_extras,
             Requirement('placeholder' + extras.lower()).extras)
        return (
         package_name, url_no_extras, None)
    for version_control in vcs:
        if url.lower().startswith('{}:'.format(version_control)):
            url = '{}+{}'.format(version_control, url)
            break

    if '+' not in url:
        raise InstallationError('{} is not a valid editable requirement. It should either be a path to a local project or a VCS URL (beginning with svn+, git+, hg+, or bzr+).'.format(editable_req))
    vc_type = url.split('+', 1)[0].lower()
    if not vcs.get_backend(vc_type):
        backends = ', '.join([bends.name + '+URL' for bends in vcs.backends])
        error_message = 'For --editable={}, only {} are currently supported'.format(editable_req, backends)
        raise InstallationError(error_message)
    package_name = Link(url).egg_fragment
    if not package_name:
        raise InstallationError("Could not detect requirement name for '{}', please specify one with #egg=your_package_name".format(editable_req))
    return (package_name, url, None)


def deduce_helpful_msg(req):
    """Returns helpful msg in case requirements file does not exist,
    or cannot be parsed.

    :params req: Requirements file path
    """
    msg = ''
    if os.path.exists(req):
        msg = ' It does exist.'
        try:
            with open(req, 'r') as (fp):
                next(parse_requirements(fp.read()))
                msg += "The argument you provided ({}) appears to be a requirements file. If that is the case, use the '-r' flag to install the packages specified within it.".format(req)
        except RequirementParseError:
            logger.debug(("Cannot parse '{}' as requirements             file".format(req)),
              exc_info=True)

    else:
        msg += " File '{}' does not exist.".format(req)
    return msg


class RequirementParts(object):

    def __init__(self, requirement, link, markers, extras):
        self.requirement = requirement
        self.link = link
        self.markers = markers
        self.extras = extras


def parse_req_from_editable(editable_req):
    name, url, extras_override = parse_editable(editable_req)
    if name is not None:
        try:
            req = Requirement(name)
        except InvalidRequirement:
            raise InstallationError("Invalid requirement: '{}'".format(name))

    else:
        req = None
    link = Link(url)
    return RequirementParts(req, link, None, extras_override)


def install_req_from_editable(editable_req, comes_from=None, use_pep517=None, isolated=False, options=None, constraint=False):
    parts = parse_req_from_editable(editable_req)
    return InstallRequirement((parts.requirement),
      comes_from=comes_from,
      editable=True,
      link=(parts.link),
      constraint=constraint,
      use_pep517=use_pep517,
      isolated=isolated,
      install_options=(options.get('install_options', []) if options else []),
      global_options=(options.get('global_options', []) if options else []),
      hash_options=(options.get('hashes', {}) if options else {}),
      extras=(parts.extras))


def _looks_like_path(name):
    """Checks whether the string "looks like" a path on the filesystem.

    This does not check whether the target actually exists, only judge from the
    appearance.

    Returns true if any of the following conditions is true:
    * a path separator is found (either os.path.sep or os.path.altsep);
    * a dot is found (which represents the current directory).
    """
    if os.path.sep in name:
        return True
    if os.path.altsep is not None:
        if os.path.altsep in name:
            return True
    if name.startswith('.'):
        return True
    return False


def _get_url_from_path(path, name):
    """
    First, it checks whether a provided path is an installable directory
    (e.g. it has a setup.py). If it is, returns the path.

    If false, check if the path is an archive file (such as a .whl).
    The function checks if the path is a file. If false, if the path has
    an @, it will treat it as a PEP 440 URL requirement and return the path.
    """
    if _looks_like_path(name):
        if os.path.isdir(path):
            if is_installable_dir(path):
                return path_to_url(path)
            raise InstallationError(("Directory {name!r} is not installable. Neither 'setup.py' nor 'pyproject.toml' found.".format)(**locals()))
    else:
        if not is_archive_file(path):
            return
        if os.path.isfile(path):
            return path_to_url(path)
        urlreq_parts = name.split('@', 1)
        if len(urlreq_parts) >= 2:
            return _looks_like_path(urlreq_parts[0]) or None
    logger.warning('Requirement %r looks like a filename, but the file does not exist', name)
    return path_to_url(path)


def parse_req_from_line(name, line_source):
    if is_url(name):
        marker_sep = '; '
    else:
        marker_sep = ';'
    if marker_sep in name:
        name, markers_as_string = name.split(marker_sep, 1)
        markers_as_string = markers_as_string.strip()
        if not markers_as_string:
            markers = None
        else:
            markers = Marker(markers_as_string)
    else:
        markers = None
    name = name.strip()
    req_as_string = None
    path = os.path.normpath(os.path.abspath(name))
    link = None
    extras_as_string = None
    if is_url(name):
        link = Link(name)
    else:
        p, extras_as_string = _strip_extras(path)
        url = _get_url_from_path(p, name)
        if url is not None:
            link = Link(url)
        elif link:
            if link.scheme == 'file':
                if re.search('\\.\\./', link.url):
                    link = Link(path_to_url(os.path.normpath(os.path.abspath(link.path))))
                elif link.is_wheel:
                    wheel = Wheel(link.filename)
                    req_as_string = ('{wheel.name}=={wheel.version}'.format)(**locals())
                else:
                    req_as_string = link.egg_fragment
            else:
                req_as_string = name
            extras = convert_extras(extras_as_string)

            def with_source(text):
                if not line_source:
                    return text
                return '{} (from {})'.format(text, line_source)

            if req_as_string is not None:
                try:
                    req = Requirement(req_as_string)
                except InvalidRequirement:
                    if os.path.sep in req_as_string:
                        add_msg = 'It looks like a path.'
                        add_msg += deduce_helpful_msg(req_as_string)
                    else:
                        if '=' in req_as_string:
                            add_msg = any((op in req_as_string for op in operators)) or '= is not a valid operator. Did you mean == ?'
                        else:
                            add_msg = ''
                    msg = with_source('Invalid requirement: {!r}'.format(req_as_string))
                    if add_msg:
                        msg += '\nHint: {}'.format(add_msg)
                    raise InstallationError(msg)

        else:
            req = None
        return RequirementParts(req, link, markers, extras)


def install_req_from_line(name, comes_from=None, use_pep517=None, isolated=False, options=None, constraint=False, line_source=None):
    """Creates an InstallRequirement from a name, which might be a
    requirement, directory containing 'setup.py', filename, or URL.

    :param line_source: An optional string describing where the line is from,
        for logging purposes in case of an error.
    """
    parts = parse_req_from_line(name, line_source)
    return InstallRequirement((parts.requirement),
      comes_from, link=(parts.link), markers=(parts.markers), use_pep517=use_pep517,
      isolated=isolated,
      install_options=(options.get('install_options', []) if options else []),
      global_options=(options.get('global_options', []) if options else []),
      hash_options=(options.get('hashes', {}) if options else {}),
      constraint=constraint,
      extras=(parts.extras))


def install_req_from_req_string(req_string, comes_from=None, isolated=False, use_pep517=None):
    try:
        req = Requirement(req_string)
    except InvalidRequirement:
        raise InstallationError("Invalid requirement: '{}'".format(req_string))

    domains_not_allowed = [
     PyPI.file_storage_domain,
     TestPyPI.file_storage_domain]
    if req.url:
        if comes_from:
            if comes_from.link:
                if comes_from.link.netloc in domains_not_allowed:
                    raise InstallationError('Packages installed from PyPI cannot depend on packages which are not also hosted on PyPI.\n{} depends on {} '.format(comes_from.name, req))
    return InstallRequirement(req,
      comes_from, isolated=isolated, use_pep517=use_pep517)


def install_req_from_parsed_requirement(parsed_req, isolated=False, use_pep517=None):
    if parsed_req.is_editable:
        req = install_req_from_editable((parsed_req.requirement),
          comes_from=(parsed_req.comes_from),
          use_pep517=use_pep517,
          constraint=(parsed_req.constraint),
          isolated=isolated)
    else:
        req = install_req_from_line((parsed_req.requirement),
          comes_from=(parsed_req.comes_from),
          use_pep517=use_pep517,
          isolated=isolated,
          options=(parsed_req.options),
          constraint=(parsed_req.constraint),
          line_source=(parsed_req.line_source))
    return req