# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/backports/email/policy.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 8823 bytes
"""This will be the home for the policy that hooks in the new
code that adds all the email6 features.
"""
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import super
from future.standard_library.email._policybase import Policy, Compat32, compat32, _extend_docstrings
from future.standard_library.email.utils import _has_surrogates
from future.standard_library.email.headerregistry import HeaderRegistry
__all__ = [
 'Compat32',
 'compat32',
 'Policy',
 'EmailPolicy',
 'default',
 'strict',
 'SMTP',
 'HTTP']

@_extend_docstrings
class EmailPolicy(Policy):
    __doc__ = "+\n    PROVISIONAL\n\n    The API extensions enabled by this policy are currently provisional.\n    Refer to the documentation for details.\n\n    This policy adds new header parsing and folding algorithms.  Instead of\n    simple strings, headers are custom objects with custom attributes\n    depending on the type of the field.  The folding algorithm fully\n    implements RFCs 2047 and 5322.\n\n    In addition to the settable attributes listed above that apply to\n    all Policies, this policy adds the following additional attributes:\n\n    refold_source       -- if the value for a header in the Message object\n                           came from the parsing of some source, this attribute\n                           indicates whether or not a generator should refold\n                           that value when transforming the message back into\n                           stream form.  The possible values are:\n\n                           none  -- all source values use original folding\n                           long  -- source values that have any line that is\n                                    longer than max_line_length will be\n                                    refolded\n                           all  -- all values are refolded.\n\n                           The default is 'long'.\n\n    header_factory      -- a callable that takes two arguments, 'name' and\n                           'value', where 'name' is a header field name and\n                           'value' is an unfolded header field value, and\n                           returns a string-like object that represents that\n                           header.  A default header_factory is provided that\n                           understands some of the RFC5322 header field types.\n                           (Currently address fields and date fields have\n                           special treatment, while all other fields are\n                           treated as unstructured.  This list will be\n                           completed before the extension is marked stable.)\n    "
    refold_source = 'long'
    header_factory = HeaderRegistry()

    def __init__(self, **kw):
        if 'header_factory' not in kw:
            object.__setattr__(self, 'header_factory', HeaderRegistry())
        super().__init__(**kw)

    def header_max_count(self, name):
        """+
        The implementation for this class returns the max_count attribute from
        the specialized header class that would be used to construct a header
        of type 'name'.
        """
        return self.header_factory[name].max_count

    def header_source_parse(self, sourcelines):
        """+
        The name is parsed as everything up to the ':' and returned unmodified.
        The value is determined by stripping leading whitespace off the
        remainder of the first line, joining all subsequent lines together, and
        stripping any trailing carriage return or linefeed characters.  (This
        is the same as Compat32).

        """
        name, value = sourcelines[0].split(':', 1)
        value = value.lstrip(' \t') + ''.join(sourcelines[1:])
        return (name, value.rstrip('\r\n'))

    def header_store_parse(self, name, value):
        """+
        The name is returned unchanged.  If the input value has a 'name'
        attribute and it matches the name ignoring case, the value is returned
        unchanged.  Otherwise the name and value are passed to header_factory
        method, and the resulting custom header object is returned as the
        value.  In this case a ValueError is raised if the input value contains
        CR or LF characters.

        """
        if hasattr(value, 'name') and value.name.lower() == name.lower():
            return (name, value)
        if isinstance(value, str) and len(value.splitlines()) > 1:
            raise ValueError('Header values may not contain linefeed or carriage return characters')
        return (name, self.header_factory(name, value))

    def header_fetch_parse(self, name, value):
        """+
        If the value has a 'name' attribute, it is returned to unmodified.
        Otherwise the name and the value with any linesep characters removed
        are passed to the header_factory method, and the resulting custom
        header object is returned.  Any surrogateescaped bytes get turned
        into the unicode unknown-character glyph.

        """
        if hasattr(value, 'name'):
            return value
        return self.header_factory(name, ''.join(value.splitlines()))

    def fold(self, name, value):
        """+
        Header folding is controlled by the refold_source policy setting.  A
        value is considered to be a 'source value' if and only if it does not
        have a 'name' attribute (having a 'name' attribute means it is a header
        object of some sort).  If a source value needs to be refolded according
        to the policy, it is converted into a custom header object by passing
        the name and the value with any linesep characters removed to the
        header_factory method.  Folding of a custom header object is done by
        calling its fold method with the current policy.

        Source values are split into lines using splitlines.  If the value is
        not to be refolded, the lines are rejoined using the linesep from the
        policy and returned.  The exception is lines containing non-ascii
        binary data.  In that case the value is refolded regardless of the
        refold_source setting, which causes the binary data to be CTE encoded
        using the unknown-8bit charset.

        """
        return self._fold(name, value, refold_binary=True)

    def fold_binary(self, name, value):
        """+
        The same as fold if cte_type is 7bit, except that the returned value is
        bytes.

        If cte_type is 8bit, non-ASCII binary data is converted back into
        bytes.  Headers with binary data are not refolded, regardless of the
        refold_header setting, since there is no way to know whether the binary
        data consists of single byte characters or multibyte characters.

        """
        folded = self._fold(name, value, refold_binary=self.cte_type == '7bit')
        return folded.encode('ascii', 'surrogateescape')

    def _fold(self, name, value, refold_binary=False):
        if hasattr(value, 'name'):
            return value.fold(policy=self)
        maxlen = self.max_line_length if self.max_line_length else float('inf')
        lines = value.splitlines()
        refold = self.refold_source == 'all' or self.refold_source == 'long' and (lines and len(lines[0]) + len(name) + 2 > maxlen or any(len(x) > maxlen for x in lines[1:]))
        if refold or refold_binary and _has_surrogates(value):
            return self.header_factory(name, ''.join(lines)).fold(policy=self)
        return name + ': ' + self.linesep.join(lines) + self.linesep


default = EmailPolicy()
del default.header_factory
strict = default.clone(raise_on_defect=True)
SMTP = default.clone(linesep='\r\n')
HTTP = default.clone(linesep='\r\n', max_line_length=None)