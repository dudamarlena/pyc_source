# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/build/step/step/step.py
# Compiled at: 2019-10-10 16:44:46
"""A light and fast template engine."""
import re, sys
PY3 = False
if sys.version_info > (3, 0):
    PY3 = True

class Template(object):
    COMPILED_TEMPLATES = {}
    RE_STRIP = re.compile('(^[ \t]+|[ \t]+$|(?<=[ \t])[ \t]+|\\A[\r\n]+|[ \t\r\n]+\\Z)', re.M)

    def __init__(self, template, strip=True):
        """Initialize class"""
        super(Template, self).__init__()
        self.template = template
        self.options = {'strip': strip}
        self.builtins = {'escape': lambda s: escape_html(s), 'setopt': lambda k, v: self.options.update({k: v})}
        if template in Template.COMPILED_TEMPLATES:
            self.code = Template.COMPILED_TEMPLATES[template]
        else:
            self.code = self._process(self._preprocess(self.template))
            Template.COMPILED_TEMPLATES[template] = self.code

    def expand(self, namespace={}, **kw):
        """Return the expanded template string"""
        output = []
        namespace.update(kw, **self.builtins)
        namespace['echo'] = lambda s: output.append(s)
        namespace['isdef'] = lambda v: v in namespace
        eval(compile(self.code, '<string>', 'exec'), namespace)
        return self._postprocess(('').join(map(to_unicode, output)))

    def stream(self, buffer, namespace={}, encoding='utf-8', **kw):
        """Expand the template and stream it to a file-like buffer."""

        def write_buffer(s, flush=False, cache=['']):
            cache[0] += to_unicode(s)
            if flush and cache[0] or len(cache[0]) > 65536:
                buffer.write(postprocess(cache[0]))
                cache[0] = ''

        namespace.update(kw, **self.builtins)
        namespace['echo'] = write_buffer
        namespace['isdef'] = lambda v: v in namespace
        postprocess = lambda s: s.encode(encoding)
        if self.options['strip']:
            postprocess = lambda s: Template.RE_STRIP.sub('', s).encode(encoding)
        eval(compile(self.code, '<string>', 'exec'), namespace)
        write_buffer('', flush=True)

    def _preprocess(self, template):
        """Modify template string before code conversion"""
        o = re.compile('(?m)^[ \t]*%((if|for|while|try).+:)')
        c = re.compile('(?m)^[ \t]*%(((else|elif|except|finally).*:)|(end\\w+))')
        template = c.sub('<%:\\g<1>%>', o.sub('<%\\g<1>%>', template))
        v = re.compile('\\{\\{(.*?)\\}\\}')
        template = v.sub('<%echo(\\g<1>)%>\\n', template)
        return template

    def _process(self, template):
        """Return the code generated from the template string"""
        code_blk = re.compile('<%(.*?)%>\\n?', re.DOTALL)
        indent = 0
        code = []
        for n, blk in enumerate(code_blk.split(template)):
            blk = re.sub('<\\\\%', '<%', re.sub('%\\\\>', '%>', blk))
            blk = re.sub('\\\\(%|{|})', '\\g<1>', blk)
            if not n % 2:
                blk = re.sub('\\\\', '\\\\\\\\', blk)
                blk = re.sub('"', '\\\\"', blk)
                blk = ' ' * (indent * 4) + ('echo("""{0}""")').format(blk)
            else:
                blk = blk.rstrip()
                if blk.lstrip().startswith(':'):
                    if not indent:
                        err = 'unexpected block ending'
                        raise SyntaxError(('Line {0}: {1}').format(n, err))
                    indent -= 1
                    if blk.startswith(':end'):
                        continue
                    blk = blk.lstrip()[1:]
                blk = re.sub('(?m)^', ' ' * (indent * 4), blk)
                if blk.endswith(':'):
                    indent += 1
            code.append(blk)

        if indent:
            err = 'Reached EOF before closing block'
            raise EOFError(('Line {0}: {1}').format(n, err))
        return ('\n').join(code)

    def _postprocess(self, output):
        """Modify output string after variables and code evaluation"""
        if self.options['strip']:
            output = Template.RE_STRIP.sub('', output)
        return output


def escape_html(x):
    """Escape HTML special characters &<> and quotes "'."""
    CHARS, ENTITIES = '&<>"\'', ['&amp;', '&lt;', '&gt;', '&quot;', '&#39;']
    string = x if isinstance(x, basestring) else str(x)
    for c, e in zip(CHARS, ENTITIES):
        string = string.replace(c, e)

    return string


def to_unicode(x, encoding='utf-8'):
    """Convert anything to Unicode."""
    if PY3:
        return str(x)
    if not isinstance(x, unicode):
        x = unicode(str(x), encoding, errors='replace')
    return x