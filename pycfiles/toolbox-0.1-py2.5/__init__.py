# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/toolbox/__init__.py
# Compiled at: 2009-10-08 23:07:02
import os, re, logging, exceptions
from optparse import OptionParser
if os.getenv('DEBUG') is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARN)

class toolbox(object):
    log = logging.getLogger('toolbox.toolbox')

    def __init__(self, toolbox_dir=None):
        super(toolbox, self).__init__()
        if toolbox_dir is None:
            toolbox_dir = self.__find_toolbox_dir()
        self.__tooldir = tooldir(toolbox_dir)
        self.__tools = self.__tooldir.generate_tools()
        return

    def __find_toolbox_dir(self):
        return os.path.expanduser('~/tools')

    @property
    def tooldir(self):
        """docstring for tooldir"""
        return self.__tooldir

    def list(self, args=[]):
        """docstring for list"""
        if len(args) == 0:
            for tool in self.__tools.keys():
                print '%s' % tool

        elif args[0] in self.__tools.keys():
            print 'Current version: %s' % self.__tools[args[0]].version
            print 'Available versions:'
            for version in self.__tools[args[0]].available_versions:
                print '\t%s' % version

        else:
            print 'No such tool.'
        return True

    def switch(self, args=[]):
        """docstring for switch"""
        if len(args) < 2:
            print 'Switching versions requires a tool name and a version.'
            return False
        toolname = args[0]
        version = args[1]
        if args[0] not in self.__tools.keys():
            print 'No such tool.'
            return True
        if version in self.__tools[toolname].available_versions:
            self.__tools[toolname].set_version(version)
            print '%s %s active.' % (toolname, version)
            return True
        else:
            print 'Version does not exist for tool: %s.' % toolname
            return self.list([toolname])


class tool(object):
    log = logging.getLogger('toolbox.tool')

    def __init__(self, name, basepath):
        """docstring for __init__"""
        super(tool, self).__init__()
        tool.log.debug('creating %s' % name)
        self.__name = name
        self.__basepath = basepath
        self.__versions = {}
        self.__current_version = None
        self.__find_versions(basepath)
        return

    @property
    def name(self):
        """docstring for name"""
        return self.__name

    def __find_versions(self, path):
        """docstring for __find_versions"""
        regx = re.compile('^(?:apache-)?%s-(?:bin-)?(\\d[\\d\\.]+[a-z\\d]?)$' % self.name)
        dirs = os.listdir(path)
        for d in dirs:
            tool.log.debug('__f_v: %s' % d)
            if re.search(regx, d):
                if d == self.name:
                    target = os.path.basename(os.readlink(os.path.join(path, d)))
                    match = re.search(regx, target)
                    if match is not None:
                        self.__current_version = match.group(1)
                elif os.path.isdir(os.path.join(path, d)) and not os.path.islink(os.path.join(path, d)):
                    match = re.search(regx, d)
                    if match is not None:
                        version = match.group(1)
                        self.__add_version(version, os.path.join(path, d))

        return

    def __find_current_version(self, path):
        """docstring for __find_current_version"""
        symlink = os.path.join(path, self.name)

    def __add_version(self, version, path):
        """docstring for __add_version"""
        tool.log.debug('__a_v: %s %s %s' % (self.name, version, path))
        self.__versions[version] = path

    def __update_symlink(self):
        """docstring for __update_symlink"""
        path = self.__basepath
        version = self.get_version()
        symlink = os.path.join(path, self.name)
        target_dir = self.__versions[version]
        tool.log.debug('__u_s: target_dir %s' % target_dir)
        if os.path.isdir(target_dir) and not os.path.islink(target_dir):
            tool.log.debug('__u_s: target_dir valid')
            if os.path.islink(symlink):
                tool.log.debug('__u_s: removing symlink')
                os.remove(symlink)
            os.symlink(target_dir, symlink)
            tool.log.debug('__u_s: creating symlink')
        else:
            raise InvalidSymlinkError

    def get_version(self):
        """docstring for get_version"""
        return self.__current_version

    def set_version(self, version_number):
        """docstring for set_version"""
        if self.__current_version == version_number:
            return
        if version_number in self.available_versions:
            self.__current_version = version_number
            self.__update_symlink()
        else:
            raise InvalidVersionError

    version = property(get_version, set_version)

    @property
    def available_versions(self):
        """docstring for available_versions"""
        return self.__versions.keys()


class tooldir(object):
    """docstring for tooldir_reader"""
    log = logging.getLogger('toolbox.tooldir')
    regx = re.compile('^(?:apache-)?([a-z\\-]+)-(?:bin-)?(\\d[\\d\\.]+[a-z\\d]?)$')

    def __init__(self, path):
        super(tooldir, self).__init__()
        self.__path = os.path.abspath(path)
        self.__directories = []
        self.__symlinks = []
        self.__read_tooldir()

    def __read_tooldir(self):
        """docstring for __read_tooldir"""
        for item in os.listdir(self.path):
            tooldir.log.debug('__r_t: %s' % item)
            if re.match(tooldir.regx, item):
                fullitem = os.path.join(self.path, item)
                if os.path.islink(fullitem):
                    self.__symlinks.append(fullitem)
                elif os.path.isdir(fullitem):
                    self.__directories.append(fullitem)

    def generate_tools(self):
        """docstring for generate_tools"""
        tools = {}
        for itemdir in self.__directories:
            item = os.path.basename(itemdir)
            tooldir.log.debug('g_t: %s' % item)
            m = re.search(tooldir.regx, item)
            tooldir.log.debug(m)
            if m is not None and m.group(1) not in tools.keys():
                tools[m.group(1)] = tool(m.group(1), self.__path)

        return tools

    @property
    def path(self):
        """docstring for path"""
        return self.__path


class InvalidVersionError(exceptions.RuntimeError):
    pass


class InvalidSymlinkError(exceptions.RuntimeError):
    pass


def run_script():
    usage = 'usage: %prog [options] toolname [version]'
    parser = OptionParser(usage=usage)
    parser.add_option('-v', action='store_true', dest='verbose', default=True)
    parser.add_option('-q', action='store_false', dest='verbose')
    parser.add_option('-d', action='store', type='string', dest='toolbox_dir', default=None)
    parser.add_option('-l', '--list', action='store_const', dest='action', const='list', default='switch')
    (options, args) = parser.parse_args()
    tbx = toolbox(options.toolbox_dir)
    try:
        method = getattr(tbx, options.action, None)
        if not method(args):
            parser.print_help()
    except:
        parser.print_help()

    return