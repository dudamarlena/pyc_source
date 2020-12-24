# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/console.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import getpass, logging, os, subprocess, sys
from distutils.util import strtobool
from six.moves import input
from rbtools.utils.encoding import force_unicode
from rbtools.utils.errors import EditorError
from rbtools.utils.filesystem import make_tempfile
logger = logging.getLogger(__name__)

def get_input(prompt, require=False):
    """Ask the user for input.

    Args:
        prompt (unicode):
            The text to prompt the user with.

        require (bool, optional):
            Whether to require a result. If ``True``, this will keep prompting
            until a non-empty value is entered.

    Returns:
        unicode:
        The entered user data.
    """

    def _get_input():
        sys.stderr.write(prompt)
        return input()

    prompt = str(prompt)
    if require:
        value = None
        while not value:
            value = _get_input()

    else:
        value = _get_input()
    return value


def get_pass(prompt, require=False):
    """Ask the user for a password.

    Args:
        prompt (unicode):
            The text to prompt the user with.

        require (bool, optional):
            Whether to require a result. If ``True``, this will keep prompting
            until a non-empty value is entered.

    Returns:
        bytes:
        The entered password.
    """
    prompt = str(prompt)
    if require:
        password = None
        while not password:
            password = getpass.getpass(prompt)

    else:
        password = getpass.getpass(prompt)
    return password


def confirm(question):
    """Interactively prompt for a Yes/No answer.

    Accepted values (case-insensitive) depend on distutils.util.strtobool():
    'Yes' values: y, yes, t, true, on, 1
    'No' values: n, no , f, false, off, 0
    """
    while True:
        full_question = b'%s [Yes/No]: ' % question
        answer = get_input(full_question).lower()
        try:
            return strtobool(answer)
        except ValueError:
            print(b'%s is not a valid answer.' % answer)


def edit_file(filename):
    """Run a user-configured editor to edit an existing file.

    This will run a configured text editor (trying the :envvar:`VISUAL` or
    :envvar:`EDITOR` environment variables, falling back on :program:`vi`)
    to request text for use in a commit message or some other purpose.

    Args:
        filename (unicode):
            The file to edit.

    Returns:
        unicode:
        The resulting content.

    Raises:
        rbcommons.utils.errors.EditorError:
            The configured editor could not be run, or it failed with an
            error.
    """
    if not os.path.exists(filename):
        raise EditorError(b'The file "%s" does not exist or is not accessible.' % filename)
    editor = force_unicode(os.environ.get(str(b'RBTOOLS_EDITOR')) or os.environ.get(str(b'VISUAL')) or os.environ.get(str(b'EDITOR')) or b'vi')
    try:
        subprocess.call(editor.split() + [filename])
    except OSError:
        raise EditorError(b'The editor "%s" was not found or could not be run. Make sure the EDITOR environment variable is set to your preferred editor.' % editor)

    try:
        with open(filename, b'r') as (fp):
            return force_unicode(fp.read())
    except IOError:
        raise EditorError(b'The edited file "%s" was deleted during edit.' % filename)


def edit_text(content=b'', filename=None):
    """Run a user-configured editor to prompt for text.

    This will run a configured text editor (trying the :envvar:`VISUAL` or
    :envvar:`EDITOR` environment variables, falling back on :program:`vi`)
    to request text for use in a commit message or some other purpose.

    Args:
        content (unicode, optional):
            Existing content to edit.

        filename (unicode, optional):
            The optional name of the temp file to edit. This can be used to
            help the editor provide a proper editing environment for the
            file.

    Returns:
        unicode:
        The resulting content.

    Raises:
        rbcommons.utils.errors.EditorError:
            The configured editor could not be run, or it failed with an
            error.
    """
    tempfile = make_tempfile(content.encode(b'utf8'), filename=filename)
    result = edit_file(tempfile)
    os.unlink(tempfile)
    return result