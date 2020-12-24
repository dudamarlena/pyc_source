# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/utils.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1937 bytes
"""Module for test utilities."""
import re, time
from typing import Any, Callable, Union

class RegexCompare:
    __doc__ = '\n    Class for creating regex objects which can be compared with strings.\n\n    :param regex: Regex string pattern"\n    '

    def __init__(self, regex: str) -> None:
        """Constructor for RegexCompare object."""
        self.pattern = re.compile(regex)

    def __eq__(self, other) -> bool:
        """Return True if full regex match."""
        assert isinstance(other, str)
        return bool(self.pattern.fullmatch(other))

    def __repr__(self) -> str:
        """Return string representation of RegexCompare object."""
        return f"RegexCompare({self.pattern})"


class Retry:
    __doc__ = '\n    Class for retrying tests.\n\n    :param expression: Zero arity callable which should return True after some\n        retries.\n    :param tries: Number of attempts.\n    :param delay: Seconds to sleep between each attempt.\n    :param increase_delay: Increase delay for each attempt.\n    '

    def __init__(self, tries: int=10, delay: Union[(int, float)]=0.1, increase_delay: Union[(int, float)]=0.3) -> None:
        """Retry object constructor."""
        self.tries = tries
        self.delay = delay
        self.increase = increase_delay

    def __call__(self, expression: Callable[([], Any)]) -> bool:
        """
        Retry callable until it returns a truthy value.

        :param expression: Zero arity callable returning truhty/falsy values.
        """
        attempt = 0
        while attempt < self.tries:
            attempt += 1
            try:
                result = expression()
                if result:
                    return result
            except BaseException:
                pass

            time.sleep(self.delay)
            self.delay += self.increase

        return expression()