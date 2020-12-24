# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/utils/user_agent.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 4524 bytes
import collections, platform, sys

def user_agent(name, version, extras=None):
    """Return an internet-friendly user_agent string.

    The majority of this code has been wilfully stolen from the equivalent
    function in Requests.

    :param name: The intended name of the user-agent, e.g. "python-requests".
    :param version: The version of the user-agent, e.g. "0.0.1".
    :param extras: List of two-item tuples that are added to the user-agent
        string.
    :returns: Formatted user-agent string
    :rtype: str
    """
    if extras is None:
        extras = []
    return UserAgentBuilder(name, version).include_extras(extras).include_implementation().include_system().build()


class UserAgentBuilder(object):
    __doc__ = "Class to provide a greater level of control than :func:`user_agent`.\n\n    This is used by :func:`user_agent` to build its User-Agent string.\n\n    .. code-block:: python\n\n        user_agent_str = UserAgentBuilder(\n                name='requests-toolbelt',\n                version='17.4.0',\n            ).include_implementation(\n            ).include_system(\n            ).include_extras([\n                ('requests', '2.14.2'),\n                ('urllib3', '1.21.2'),\n            ]).build()\n\n    "
    format_string = '%s/%s'

    def __init__(self, name, version):
        """Initialize our builder with the name and version of our user agent.

        :param str name:
            Name of our user-agent.
        :param str version:
            The version string for user-agent.
        """
        self._pieces = collections.deque([(name, version)])

    def build(self):
        """Finalize the User-Agent string.

        :returns:
            Formatted User-Agent string.
        :rtype:
            str
        """
        return ' '.join([self.format_string % piece for piece in self._pieces])

    def include_extras(self, extras):
        """Include extra portions of the User-Agent.

        :param list extras:
            list of tuples of extra-name and extra-version
        """
        if any(len(extra) != 2 for extra in extras):
            raise ValueError('Extras should be a sequence of two item tuples.')
        self._pieces.extend(extras)
        return self

    def include_implementation(self):
        """Append the implementation string to the user-agent string.

        This adds the the information that you're using CPython 2.7.13 to the
        User-Agent.
        """
        self._pieces.append(_implementation_tuple())
        return self

    def include_system(self):
        """Append the information about the Operating System."""
        self._pieces.append(_platform_tuple())
        return self


def _implementation_tuple():
    """Return the tuple of interpreter name and version.

    Returns a string that provides both the name and the version of the Python
    implementation currently running. For example, on CPython 2.7.5 it will
    return "CPython/2.7.5".

    This function works best on CPython and PyPy: in particular, it probably
    doesn't work for Jython or IronPython. Future investigation should be done
    to work out the correct shape of the code for those platforms.
    """
    implementation = platform.python_implementation()
    if implementation == 'CPython':
        implementation_version = platform.python_version()
    else:
        if implementation == 'PyPy':
            implementation_version = '%s.%s.%s' % (sys.pypy_version_info.major,
             sys.pypy_version_info.minor,
             sys.pypy_version_info.micro)
            if sys.pypy_version_info.releaselevel != 'final':
                implementation_version = ''.join([
                 implementation_version, sys.pypy_version_info.releaselevel])
        else:
            if implementation == 'Jython':
                implementation_version = platform.python_version()
            else:
                if implementation == 'IronPython':
                    implementation_version = platform.python_version()
                else:
                    implementation_version = 'Unknown'
    return (
     implementation, implementation_version)


def _implementation_string():
    return '%s/%s' % _implementation_tuple()


def _platform_tuple():
    try:
        p_system = platform.system()
        p_release = platform.release()
    except IOError:
        p_system = 'Unknown'
        p_release = 'Unknown'

    return (
     p_system, p_release)