# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ake/projects/python/lingua-franca/lingua_franca/__init__.py
# Compiled at: 2019-10-30 03:15:00
# Size of source mod 2**32: 2263 bytes
import os
from os.path import join, expanduser

def _log_unsupported_language(language, supported_languages):
    """
    Log a warning when a language is unsupported

    Arguments:
        language: str
            The language that was supplied.
        supported_languages: [str]
            The list of supported languages.
    """
    supported = ' '.join(supported_languages)
    print('Language "{language}" not recognized! Please make sure your language is one of the following: {supported}.'.format(language=language,
      supported=supported))


def resolve_resource_file(res_name, data_dir=None):
    """Convert a resource into an absolute filename.

    Resource names are in the form: 'filename.ext'
    or 'path/filename.ext'

    The system wil look for ~/.mycroft/res_name first, and
    if not found will look at /opt/mycroft/res_name,
    then finally it will look for res_name in the 'mycroft/res'
    folder of the source code package.

    Example:
    With mycroft running as the user 'bob', if you called
        resolve_resource_file('snd/beep.wav')
    it would return either '/home/bob/.mycroft/snd/beep.wav' or
    '/opt/mycroft/snd/beep.wav' or '.../mycroft/res/snd/beep.wav',
    where the '...' is replaced by the path where the package has
    been installed.

    Args:
        res_name (str): a resource path/name
    Returns:
        str: path to resource or None if no resource found
    """
    if os.path.isfile(res_name):
        return res_name
    filename = os.path.expanduser('~/.mycroft/' + res_name)
    if os.path.isfile(filename):
        return filename
    data_dir = data_dir or expanduser('/opt/mycroft/res/')
    filename = os.path.expanduser(join(data_dir, res_name))
    if os.path.isfile(filename):
        return filename
    filename = os.path.join(os.path.dirname(__file__), 'res', res_name)
    filename = os.path.abspath(os.path.normpath(filename))
    if os.path.isfile(filename):
        return filename