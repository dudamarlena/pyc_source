# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugins/fileinfo_inv_plugin_spotlight.py
# Compiled at: 2009-05-08 06:59:59
"""A fileinfo plug-in for accessing the Spotlight database on Mac OS X.

This calls a tool named 'mdls' which exists only on Mac OS X. This is 
very experimental and the function parsing the output of 'mdls' needs 
to be further debugged and completed.
"""
import sys, os.path, re, commands
from pprint import pprint as pp
from fileinfo.investigator import BaseInvestigator

def parseKmdOutput_single_attr(path, attrName):
    """Run Spotlight 'mdls' command on a file and return result for single attr."""
    output = commands.getoutput(str('mdls -name %s %s' % (attrName, path)))
    m = re.match('(\\w+) *= *(.*)', output)
    if m:
        (name, val) = m.groups()
        try:
            val = eval(val)
        except (SyntaxError, NameError):
            pass

    else:
        val = None
    print '***', path, attrName, val
    return val


def _parseKmdOutput(path):
    """Run Spotlight 'mdls' command on a file and return result as a Python dict."""
    output = commands.getoutput(str('mdls ' + path))
    print '***', output
    s = output.replace('\n', '')
    for name in ('org_python_functions', 'org_python_classes'):
        s = s.replace(name, 'kMDItem' + name)

    kmdLines = s.split('kMD')
    kmdLines = [ line for line in kmdLines if line ]
    items = [ re.match('(\\w+) *= *(.*)', line) for line in kmdLines ]
    items = [ m.groups() for m in items if m ]
    items = [ ('kMD' + k, v) for (k, v) in items ]
    pairs = []
    for item in items:
        try:
            (k, v) = item
        except:
            raise

        v = v.strip()
        try:
            ev = eval(v)
        except:
            if v[0] not in ('"', "'"):
                v = v.replace('"', '')
                v = v.replace("'", '')
            if v.startswith('('):
                v = re.sub('(\\w+)', lambda m: '"%s"' % m.groups()[0], v)

        try:
            pairs.append([k, eval(v)])
        except SyntaxError:
            pairs.append([k, v])

    data = dict(pairs)
    return data


class SpotlightInvestigator(BaseInvestigator):
    """A class for determining Mac OS X Spotlight attributes of files."""
    __module__ = __name__
    attrMap = {'kMDItem.*': 'getkMDItem', 'kMDItemKind': 'getkMDItemKind'}
    totals = ('kMDItemDurationSeconds', 'kMDItemNumberOfPages')

    def activate(self):
        """Try activating self, setting 'active' variable."""
        self.active = False
        if sys.platform == 'darwin':
            self.active = True
        return self.active

    def getkMDItem(self, attrName):
        """Return any Spotlight attribute like 'kMDItemKind'."""
        item = parseKmdOutput_single_attr(self.path, attrName)
        return item

    def getkMDItemKind(self):
        """Return Spotlight attribute 'kMDItemKind'."""
        item = self.mdDict['kMDItemKind']
        return item