# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/commands.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
import six
DEFAULT_OPTIONS_MAP = {b'debug': b'--debug', 
   b'server': b'--server', 
   b'enable_proxy': b'--disable-proxy', 
   b'disable_ssl_verification': b'--disable-ssl-verification', 
   b'username': b'--username', 
   b'password': b'--password', 
   b'api_token': b'--api-token', 
   b'repository_name': b'--repository', 
   b'repository_url': b'--repository-url', 
   b'repository_type': b'--repository-type'}
STAMP_STRING_FORMAT = b'Reviewed at %s'

class AlreadyStampedError(Exception):
    """An error indicating the change has already been stamped."""
    pass


def extract_commit_message(review_request):
    """Returns a commit message based on the review request.

    The commit message returned contains the Summary, Description, Bugs,
    and Testing Done fields from the review request, if available.
    """
    info = []
    summary = review_request.summary
    description = review_request.description
    testing_done = review_request.testing_done
    if not description.startswith(summary):
        info.append(summary)
    info.append(description)
    if testing_done:
        info.append(b'Testing Done:\n%s' % testing_done)
    if review_request.bugs_closed:
        info.append(b'Bugs closed: %s' % (b', ').join(review_request.bugs_closed))
    info.append(STAMP_STRING_FORMAT % review_request.absolute_url)
    return (b'\n\n').join(info)


def build_rbtools_cmd_argv(options, options_map=DEFAULT_OPTIONS_MAP):
    """Generates a list of command line arguments from parsed command options.

    Used for building command line arguments from existing options, when
    calling another RBTools command. ``options_map`` specifies the options
    and their corresponding argument names that need to be included.
    """
    argv = []
    for option_key, arg_name in six.iteritems(options_map):
        option_value = getattr(options, option_key, None)
        if option_value is True and option_key != b'enable_proxy':
            argv.append(arg_name)
        elif option_value not in (True, False, None):
            argv.extend([arg_name, option_value])

    if b'enable_proxy' in options_map and not options.enable_proxy:
        argv.append(options_map[b'enable_proxy'])
    return argv


def stamp_commit_with_review_url(revisions, review_request_url, tool):
    """Amend the tip revision message to include review_request_url."""
    commit_message = tool.get_raw_commit_message(revisions)
    stamp_string = STAMP_STRING_FORMAT % review_request_url
    if stamp_string in commit_message:
        raise AlreadyStampedError(b'This change is already stamped.')
    new_message = commit_message.rstrip() + b'\n\n' + stamp_string
    tool.amend_commit_description(new_message, revisions)