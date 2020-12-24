# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/dependencies.py
# Compiled at: 2020-02-11 04:03:56
"""Version information for Review Board dependencies.

This contains constants that other parts of Review Board (primarily packaging)
can use to look up information on major dependencies of Review Board.

The contents in this file might change substantially between releases. If
you're going to make use of data from this file, code defensively.
"""
from __future__ import unicode_literals
import sys, textwrap
django_doc_major_version = b'1.6'
djblets_doc_major_version = b'1.0'
django_version = b'>=1.6.11,<1.6.999'
djblets_version = b'>=1.0.12,<=1.0.999'
package_dependencies = {b'cryptography': b'>=1.8.1', 
   b'Django': django_version, 
   b'django-cors-headers': b'>=1.1.0,<1.1.999', 
   b'django_evolution': b'>=0.7.7,<=0.7.999', 
   b'django-haystack': b'>=2.4.0,<=2.4.999', 
   b'django-multiselectfield': b'', 
   b'django-oauth-toolkit': b'>=0.9.0,<0.9.999', 
   b'Djblets': djblets_version, 
   b'docutils': b'', 
   b'markdown': b'>=2.6.8,<2.6.999', 
   b'mimeparse': b'>=0.1.3', 
   b'paramiko': b'>=1.12', 
   b'Pygments': b'>=2.1', 
   b'pymdown-extensions': b'>=3.4,<3.999', 
   b'python-dateutil': b'>=1.5', 
   b'python-memcached': b'', 
   b'pytz': b'>=2015.2', 
   b'Whoosh': b'>=2.6', 
   b'requests-oauthlib': b'>=0.8,<=1.0', 
   b'django-braces': b'==1.13.0'}
package_only_dependencies = {b'rbintegrations': b'>=1.0.1'}
_dependency_error_count = 0
_dependency_warning_count = 0

def build_dependency_list(deps, version_prefix=b''):
    """Build a list of dependency specifiers from a dependency map.

    This can be used along with :py:data:`package_dependencies`,
    :py:data:`npm_dependencies`, or other dependency dictionaries to build a
    list of dependency specifiers for use on the command line or in
    :file:`setup.py`.

    Args:
        deps (dict):
            A dictionary of dependencies.

    Returns:
        list of unicode:
        A list of dependency specifiers.
    """
    return sorted([ b'%s%s%s' % (dep_name, version_prefix, dep_version) for dep_name, dep_version in deps.items()
                  ], key=lambda s: s.lower())


def _dependency_message(message, prefix=b''):
    """Utility function to print and track a dependency-related message.

    This will track that a message was printed, allowing us to determine if
    any messages were shown to the user.

    Args:
        message (unicode):
            The dependency-related message to display. This will be wrapped,
            but long strings (like paths) will not contain line breaks.

        prefix (unicode, optional):
            The prefix for the message. All text will be aligned after this.
    """
    sys.stderr.write(b'\n%s\n' % textwrap.fill(message, initial_indent=prefix, subsequent_indent=b' ' * len(prefix), break_long_words=False, break_on_hyphens=False))


def dependency_error(message):
    """Print a dependency error.

    This will track that a message was printed, allowing us to determine if
    any messages were shown to the user.

    Args:
        message (unicode):
            The dependency error to display. This will be wrapped, but long
            strings (like paths) will not contain line breaks.
    """
    global _dependency_error_count
    _dependency_message(message, prefix=b'ERROR: ')
    _dependency_error_count += 1


def dependency_warning(message):
    """Print a dependency warning.

    This will track that a message was printed, allowing us to determine if
    any messages were shown to the user.

    Args:
        message (unicode):
            The dependency warning to display. This will be wrapped, but long
            strings (like paths) will not contain line breaks.
    """
    global _dependency_warning_count
    _dependency_message(message, prefix=b'WARNING: ')
    _dependency_warning_count += 1


def fail_if_missing_dependencies():
    """Exit the process with an error if dependency messages were shown.

    If :py:func:`dependency_error` or :py:func:`dependency_warning` were
    called, this will print some help information with a link to the manual
    and then exit the process.
    """
    if _dependency_warning_count > 0 or _dependency_error_count > 0:
        from reviewboard import get_manual_url
        _dependency_message(b'Please see %s for help setting up Review Board.' % get_manual_url())
        if _dependency_error_count > 0:
            sys.exit(1)