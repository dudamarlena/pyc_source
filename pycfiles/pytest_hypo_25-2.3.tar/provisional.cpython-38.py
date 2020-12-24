# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\provisional.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 7339 bytes
"""This module contains various provisional APIs and strategies.

It is intended for internal use, to ease code reuse, and is not stable.
Point releases may move or break the contents at any time!

Internet strategies should conform to :rfc:`3986` or the authoritative
definitions it links to.  If not, report the bug!
"""
import os.path, string
import hypothesis.internal.conjecture.utils as cu
import hypothesis.strategies._internal.core as st
from hypothesis.errors import InvalidArgument
from hypothesis.strategies._internal.strategies import SearchStrategy
URL_SAFE_CHARACTERS = frozenset(string.ascii_letters + string.digits + "$-_.+!*'(),")
try:
    from importlib.resources import read_text
except ImportError:
    f = os.path.join(os.path.dirname(__file__), 'vendor', 'tlds-alpha-by-domain.txt')
    with open(f) as (tld_file):
        _tlds = tld_file.read().splitlines()
else:
    _tlds = read_text('hypothesis.vendor', 'tlds-alpha-by-domain.txt').splitlines()
assert _tlds[0].startswith('#')
TOP_LEVEL_DOMAINS = ['COM'] + sorted((_tlds[1:]), key=len)

class DomainNameStrategy(SearchStrategy):

    @staticmethod
    def clean_inputs(minimum, maximum, value, variable_name):
        if value is None:
            value = maximum
        else:
            if not isinstance(value, int):
                raise InvalidArgument('Expected integer but %s is a %s' % (
                 variable_name, type(value).__name__))
            else:
                if not minimum <= value <= maximum:
                    raise InvalidArgument('Invalid value %r < %s=%r < %r' % (
                     minimum, variable_name, value, maximum))
        return value

    def __init__(self, max_length=None, max_element_length=None):
        """
        A strategy for :rfc:`1035` fully qualified domain names.

        The upper limit for max_length is 255 in accordance with :rfc:`1035#section-2.3.4`
        The lower limit for max_length is 4, corresponding to a two letter domain
        with a single letter subdomain.
        The upper limit for max_element_length is 63 in accordance with :rfc:`1035#section-2.3.4`
        The lower limit for max_element_length is 1 in accordance with :rfc:`1035#section-2.3.4`
        """
        max_length = self.clean_inputs(4, 255, max_length, 'max_length')
        max_element_length = self.clean_inputs(1, 63, max_element_length, 'max_element_length')
        super().__init__()
        self.max_length = max_length
        self.max_element_length = max_element_length
        if self.max_element_length == 1:
            self.label_regex = '[a-zA-Z]'
        else:
            if self.max_element_length == 2:
                self.label_regex = '[a-zA-Z][a-zA-Z0-9]?'
            else:
                maximum_center_character_pattern_repetitions = self.max_element_length - 2
                self.label_regex = '[a-zA-Z]([a-zA-Z0-9\\-]{0,%d}[a-zA-Z0-9])?' % (
                 maximum_center_character_pattern_repetitions,)

    def do_draw(self, data):
        domain = data.draw(st.sampled_from(TOP_LEVEL_DOMAINS).filter(lambda tld: len(tld) + 2 <= self.max_length).flatmap(lambda tld: (st.tuples)(*[st.sampled_from([c.lower(), c.upper()]) for c in tld]).map(''.join)))
        elements = cu.many(data, min_size=1, average_size=1, max_size=126)
        while elements.more():
            sub_domain = data.draw(st.from_regex((self.label_regex), fullmatch=True))
            if len(domain) + len(sub_domain) >= self.max_length:
                data.stop_example(discard=True)
                break
            domain = sub_domain + '.' + domain

        return domain


@st.defines_strategy_with_reusable_values
def domains(max_length: int=255, max_element_length: int=63) -> SearchStrategy[str]:
    """Generate :rfc:`1035` compliant fully qualified domain names."""
    return DomainNameStrategy(max_length=max_length,
      max_element_length=max_element_length)


@st.defines_strategy_with_reusable_values
def urls() -> SearchStrategy[str]:
    """A strategy for :rfc:`3986`, generating http/https URLs."""

    def url_encode(s):
        return ''.join(((c if c in URL_SAFE_CHARACTERS else '%%%02X' % ord(c)) for c in s))

    schemes = st.sampled_from(['http', 'https'])
    ports = st.integers(min_value=0, max_value=65535).map(':{}'.format)
    paths = st.lists(st.text(string.printable).map(url_encode)).map('/'.join)
    return st.builds('{}://{}{}/{}'.format, schemes, domains(), st.just('') | ports, paths)


@st.defines_strategy_with_reusable_values
def ip4_addr_strings() -> SearchStrategy[str]:
    """A strategy for IPv4 address strings.

    This consists of four strings representing integers [0..255],
    without zero-padding, joined by dots.
    """
    return (st.builds)('{}.{}.{}.{}'.format, *4 * [st.integers(0, 255)])


@st.defines_strategy_with_reusable_values
def ip6_addr_strings() -> SearchStrategy[str]:
    """A strategy for IPv6 address strings.

    This consists of sixteen quads of hex digits (0000 .. FFFF), joined
    by colons.  Values do not currently have zero-segments collapsed.
    """
    part = st.integers(0, 65535).map('{:04x}'.format)
    return (st.tuples)(*[part] * 8).map(lambda a: ':'.join(a).upper())