# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/envgetter.py
# Compiled at: 2018-05-14 14:25:23
# Size of source mod 2**32: 12702 bytes
"""Proposed interface:

Initialize:

x=EnvGetter() or
x=EnvGetter(context='irafx') and/or
x=EnvGetter(defdict=something_besides_os_dot_environ)

Get dictionary containing environment,
  including all parent and merged with os.environ:

foo=x.envdir('/some/fully/specified/directory/')

Populate the relevant information without returning a dictionary:
x.populate('/some/fully/specified/directory/')

Write the tcas:
x.export('/some/fully/specified/directory',format='tca',fh=fh, full=False)

Export the environment as a pdk_environment file:
x.export('/some/fully/specified/directory',format='env',fh=fh, full=False)

If either .envdir or .populate have been called, you can also:

Obtain the location of the top of the tree:
top=x.gettop()

The top of the tree is defined by the presence of a file named pandokia_top.
This file is not read; it's just detected. If it is never detected, it will
go all the way to the top of the file system.
"""
import os, sys, re, warnings
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from pandokia.env_platforms import PlatformType
import pandokia.common as common
efname = 'pdk_environment'
ttop = 'pandokia_top'
pat = {'envpat':re.compile('\\${?([\\w]*?)}?(?:[\\/:]|$)'), 
 'pathkey':re.compile('[\\w]*path$', re.I), 
 'pathval':re.compile('(\\$\\{?[\\w]*path\\}?)(?:[/:]|$)', re.I)}

class FakeContainer(object):
    __doc__ = 'For testing purposes'

    def __init__(self, context=None, defdict={}, mock=False):
        self.context = context
        self.defdict = defdict
        self.platform = PlatformType()
        self.MOCK = mock


class DirLevel(object):
    __doc__ = 'Holds dictionaries and other info about the environment\n    at a given directory level'

    def __init__(self, dirname, container=None, empty=False):
        """ dirname = the name of this level
        container = the parent, usually an EnvGetter
        empty = for test purposes only, to hand-fill the object"""
        self.name = dirname
        self.container = container
        self.istop = False
        self.parent = None
        self.leveldict = {}
        self.final = {}
        self.missing = set()
        self.tca = []
        if container is None:
            self.container = FakeContainer()
        if not empty:
            self.processfile()
            self.apply_parent()
            self.merge()
            self.substitute()

    def processfile(self):
        """Process a pdk_environment file with no substitutions.
        Includes a MOCK functionality for purposes of unit testing."""
        fname = os.path.join(self.name, efname)
        if self.container.MOCK:
            self.leveldict = {'name': fname, 
             self.container.counter: self.container.counter}
            self.container.counter += 1
            if self.container.context is not None:
                print('update with context %s' % self.container.context)
        else:
            ans = parsefile(fname, self.container.platform)
            if self.container.context is not None:
                ans.update(parsefile('.'.join([fname, self.container.context]), self.container.platform))
            self.leveldict = ans
        try:
            self.tca = self.leveldict['tca'].split()
            del self.leveldict['tca']
        except KeyError:
            pass

    def apply_parent(self):
        """Applies the parent dictionary to this level's dictionary.
        Child keys always override parent keys."""
        if self.istop:
            return
        else:
            parent = os.path.dirname(self.name)
            if parent == self.name or os.path.isfile(os.path.join(self.name, ttop)):
                self.istop = True
                return
            if self.parent is None:
                self.parent = DirLevel(parent, container=(self.container))
                self.container.nodes[parent] = self.parent
        self.leveldict = dict((self.parent.leveldict), **self.leveldict)

    def merge(self):
        """Merge the current level with the default dictionary (typically
        os.environ).
           Local keys override default keys ***except*** for the
        special case of keys in the default dict that end with PATH (case-
        INsensitive), for which internal substitution will be applied."""
        self.final = dict((self.container.defdict), **self.leveldict)
        for key, val in list(self.leveldict.items()):
            try:
                if re.match(pat['pathkey'], key):
                    if ':' in val:
                        m = re.search(pat['pathval'], self.final[key])
                        if m:
                            newval = val.replace(m.group(1), self.container.defdict[key])
                            self.final[key] = newval
            except TypeError:
                pass

    def substitute(self):
        """Now that the dictionary is completely filled in, go through and
        apply the substitutions from all the values. This produces the final
        dictionary that can be supplied as the environment of a process."""
        for key, val in list(self.final.items()):
            try:
                for sub in re.findall(pat['envpat'], val):
                    self.final[key] = val.replace('$%s' % sub, self.final[sub])

            except TypeError:
                pass
            except KeyError:
                self.missing.add(sub)

    def export(self, format=None, fh=None, full=False):
        """Export the environment for this directory.

        x.export(format, file, full)

        format is one of
            'sh', 'csh'
                environment setting commands for that shell
            'env'
                as a standard pdk_environment file
            'tca'
                ???

        file is the file to write to, or sys.stdout if None

        If full, then the complete environment (including defdict,
        normally os.environ) will be exported. By default, only the
        locally- specified environment is exported.

        If the format is tca, and the tca keyword was specified in
        the environment, then its values will be used as keys into the
        defdict, and those values will be exported.
        """
        if format is None:
            format = 'tca'
        elif fh is None:
            fh = sys.stdout
        else:
            if not full:
                klist = [k for k in self.final if k not in self.container.defdict]
            else:
                klist = list(self.final.keys())
            klist.sort()
            if format == 'csh':
                for x in klist:
                    fh.write('setenv %s %s ;\n' % (
                     x,
                     common.csh_quote(self.final[x])))

                return
            if format == 'sh':
                for x in klist:
                    fh.write('%s=%s ; \n' % (x, common.sh_quote(self.final[x])))

                for x in klist:
                    fh.write('export %s ;\n' % x)

                return
            rec = dict(tca='tca_%s=%s\n', env='%s = %s\n')
            hdr = dict(tca='', env='[default]\n')
            fh.write(hdr[format])
            for key in klist:
                fh.write(rec[format] % (key, self.final[key]))

            if format == 'tca':
                if not full:
                    if len(self.tca) > 0:
                        for key in self.tca:
                            try:
                                fh.write(rec[format] % (key, self.final[key]))
                            except KeyError:
                                fh.write(rec[format] % (
                                 key, 'TCA requested but not found'))


class EnvGetter(object):
    __doc__ = 'Container class and user interface.'

    def __init__(self, defdict=None, context=None, mock=False):
        if defdict is None:
            self.defdict = os.environ.copy()
            if 'PROMPT' in self.defdict:
                del self.defdict['PROMPT']
        else:
            self.defdict = defdict
        self.nodes = dict()
        self.context = context
        self.platform = PlatformType()
        self.MOCK = mock
        self.counter = 0

    def populate(self, dirname):
        """Populates the specified level and all parents.
        If already populated, exits immediately."""
        if dirname in self.nodes:
            return
        self.nodes[dirname] = DirLevel(dirname, container=self)
        self.nodes[dirname].merge()
        self.nodes[dirname].substitute()

    def envdir(self, dirname):
        """User interface to obtain a dictionary containing a
        completely specified environment to be passed to a
        subprocess."""
        self.populate(dirname)
        if len(self.nodes[dirname].missing) > 0:
            warnings.warn('Missing values for %s. A complete environment cannot be provided for %s.' % (
             self.nodes[dirname].missing, dirname))
        return self.nodes[dirname].final

    def gettop(self):
        """Return remembered "top" of environment.
        Raise exception if more than one node thinks it is the top."""
        tlist = [v.name for v in list(self.nodes.values()) if v.istop]
        if len(tlist) == 1:
            return tlist.pop()
        raise ValueError('More than one toplevel detected: %s' % str(tlist))

    def export(self, dirname, format=None, fh=None, full=False):
        """User interface to export an environment. Delegates to
        DirLevel."""
        self.populate(dirname)
        self.nodes[dirname].export(format=format, fh=fh, full=full)


def parsefile(fname, platform=''):
    """Helper function: Make a configparser, parse the file,
    return the dictionary."""
    cfg = configparser.SafeConfigParser()
    cfg.optionxform = str
    cfg.read(fname)
    ans = {}
    try:
        for key, val in cfg.items('default'):
            ans[key] = val

    except configparser.NoSectionError:
        pass

    for section in platform:
        try:
            for key, val in cfg.items(section):
                ans[key] = val

        except configparser.NoSectionError:
            pass
        except TypeError:
            pass

    return ans