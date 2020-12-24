# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/class_info.py
# Compiled at: 2010-09-20 01:22:40
"""
Parse parameter descriptions for parser/analysis modules
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: class_info.py 25222 2010-09-20 05:22:38Z dang $'
import inspect, re
from netlogger import util
from netlogger.nllog import DoesLogging

class Info(DoesLogging):
    PARAM_RE = re.compile('-\\s*(?P<name>\\w+)\\s+(?P<values>\\{.*?\\})?\\s*:\\s*(?P<desc>.*)')

    def __init__(self, clazz):
        DoesLogging.__init__(self)
        self.desc, self.params = '', []
        for cls in inspect.getmro(clazz):
            self._extract(inspect.getdoc(cls), use_desc=cls == clazz)

        self.params.sort(key=lambda x: x.name)

    def get_desc(self):
        return self.desc

    def get_parameters(self):
        return self.params

    def _extract(self, doc, use_desc=True):
        """Extract description and parameters from the 
        docstring.
        """
        if not doc:
            return
        else:
            lines = doc.split('\n')
            state = 0
            for line in lines:
                line = line.strip()
                if state == 0:
                    if line == '':
                        state = 1
                    elif use_desc:
                        self.desc = '%s %s' % (self.desc, line)
                elif state == 1:
                    if line.startswith('Parameters:'):
                        state = 2
                elif state == 2:
                    if line.startswith('-'):
                        m = self.PARAM_RE.match(line)
                        if m is None:
                            raise ValueError('bad parameter: %s' % line)
                        d = m.groupdict()
                        p = Parameter(**d)
                        self.params.append(p)
                    elif line.endswith(':'):
                        break
                    elif self.params:
                        self.params[(-1)].add_desc(line)

            self.desc = self.desc.strip()
            return


class Parameter:
    """Encapsulate parameter attrs.
    """

    def __init__(self, name=None, values=None, desc=None):
        self.name = name
        self._desc = desc
        self.default_value = None
        self.values = []
        if len(values) > 2:
            vstr = values[1:-1]
            vv = [ s.strip() for s in vstr.split(',') ]
            for v in vv:
                if v and v[(-1)] == '*':
                    self.default_value = v[:-1]
                else:
                    self.values.append(v)

        return

    def add_desc(self, text):
        self._desc += ' %s' % text

    def _get_desc(self):
        return self._desc.strip()

    desc = property(_get_desc)