# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/utils/stringutils.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 928 bytes
import sys

def obfuscate_API_key(API_key):
    """
    Return a mostly obfuscated version of the API Key

    :param API_key: input string
    :return: str
    """
    if API_key is not None:
        return (len(API_key) - 8) * '*' + API_key[-8:]


def check_if_running_with_python_2():
    """
    Catch Python 2.x usage attempts. If Python2
    :return: `None`
    :raise: `ImportError` if running on Python 2
    """
    if sys.version_info < (3, ):
        raise ImportError('You are running PyOWM on Python 2 - how unfortunate! Since version 2.10, \nPyOWM does not support Python 2 any more. PyOWM 2.9 has however a Long-Term Support\nbranch for bug fixing on Python 2 - install it with:\n\n $ pip install git+https://github.com/csparpa/pyowm.git@v2.9-LTS\n\nThis LTS branch will be maintained until January, 1 2020\n\nSee details at:\n\nhttps://github.com/csparpa/pyowm/wiki/Timeline-for-dropping-Python-2.x-support\n\n')