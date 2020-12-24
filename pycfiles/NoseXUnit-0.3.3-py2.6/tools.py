# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/nosexunit/tools.py
# Compiled at: 2009-09-22 16:55:25
import os, pickle, logging, pkg_resources, nosexunit, nosexunit.const as nconst, nosexunit.excepts as nexcepts
logger = logging.getLogger('%s.%s' % (nconst.LOGGER, __name__))

class Singleton(object):
    """
    Singleton implementation
    On: http://www.python.org/download/releases/2.2.3/descrintro/
    """

    def __new__(cls, *args, **kwds):
        """
        Return the instance of the singleton
        Call init method if not yet initialized
        """
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        else:
            it = object.__new__(cls)
            it.init(cls, *args, **kwds)
            cls.__it__ = it
            return it

    def init(self, *args, **kwds):
        """Initialization on first call"""
        pass

    def reset(cls):
        """
        Reset the instance of the singleton
        Call close on the instance
        """
        if cls.__dict__.get('__it__') is not None:
            it = cls.__it__
            cls.__it__ = None
            it.close()
        return

    reset = staticmethod(reset)

    def close(self):
        """Close the instance of the singleton"""
        pass


def packages(root, search=False, exclude=nconst.SEARCH_EXCLUDE):
    """Return the package list contained by the folder"""
    pkgs = {}
    if os.path.exists(os.path.join(root, nconst.INIT)):
        raise nexcepts.ToolError('following folder can not contain %s file: %s' % (nconst.INIT, root))
    for (folder, folders, files) in os.walk(root):
        for bn in exclude:
            if bn in folders:
                folders.remove(bn)

        pops = []
        for fld in [ os.path.join(folder, fld) for fld in folders ]:
            if os.path.exists(os.path.join(fld, nconst.INIT)):
                entry = package(fld)
                if pkgs.has_key(entry):
                    logger.warn('package %s already exists in following folder tree: %s' % (entry, root))
                else:
                    pkgs[entry] = fld
            else:
                pops.append(os.path.basename(fld))

        if not search:
            for pop in pops:
                folders.remove(pop)

        for path in [ os.path.join(folder, fn) for fn in files ]:
            if split(path)[1] == 'py' and os.path.basename(path) != nconst.INIT:
                entry = package(path)
                if pkgs.has_key(entry):
                    logger.warn('module %s already exists in following folder tree: %s' % (entry, root))
                else:
                    pkgs[entry] = path

    return pkgs


def package(source):
    """Get the package that contains the source"""
    if not os.path.exists(source):
        raise nexcepts.ToolError("source doesn't exists: %s" % source)
    folder = os.path.dirname(source)
    base = split(os.path.basename(source))[0]
    if os.path.exists(os.path.join(folder, nconst.INIT)):
        return '%s.%s' % (package(folder), base)
    else:
        return base


def split(fn):
    """Return the extension of the provided base file"""
    sf = fn.split('.')
    l = len(sf)
    if l == 1:
        return (fn, None)
    else:
        ext = sf[(-1)]
        bn = ('.').join(sf[0:l - 1])
        return (
         bn, ext)


def save(content, path, binary=False):
    """Save the provided content in a file"""
    if binary:
        mode = 'wb'
    else:
        mode = 'w'
    fd = open(path, mode)
    fd.write(content)
    fd.close()


def load(path, binary=False):
    """Return the content of the file"""
    if binary:
        mode = 'rb'
    else:
        mode = 'r'
    fd = open(path, mode)
    content = fd.read()
    fd.close()
    return content


def create(folder):
    """Create a folder"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    elif os.path.isfile(folder):
        raise nexcepts.ToolError('following path exists but is not a folder: %s' % folder)


def clean(folder, prefix=None, ext=None):
    """Clean all file with the given extension and/or prefix in specified folder"""
    if not os.path.isdir(folder):
        raise nexcepts.ToolError("folder doesn't exist: %s" % folder)
    for bn in os.listdir(folder):
        full = os.path.join(folder, bn)
        if os.path.isfile(full) and (not prefix or prefix and bn.startswith(prefix)) and (not ext or ext and split(bn)[1] == ext):
            os.remove(full)


def get_test_id(test):
    """Get the ID of the provided test"""
    try:
        return test.id()
    except:
        entry = 'nose.nose'
        try:
            import uuid
            return '%s.%s' % (entry, uuid.uuid1())
        except:
            return '%s.%s' % (entry, id(test))


def identical(file1, file2):
    """Return True if it is the same file"""
    try:
        return os.path.samefile(file1, file2)
    except:
        return os.path.normpath(file1) == os.path.normpath(file2)


def on_posix():
    """Return True if run on POSIX platform"""
    return os.name == 'posix'


def extract(package, entry, folder, bn=None, binary=False):
    """Extract file with provided entry from the provided package"""
    content = pkg_resources.resource_string(package, entry)
    if bn:
        path = os.path.join(folder, bn)
    else:
        path = os.path.join(folder, entry)
    save(content, path, binary=binary)


def kiding(package, entry, folder, bn=None, output='html', **kwarg):
    """Extract file with provided entry from the provided package and process the template"""
    import kid
    content = pkg_resources.resource_string(package, entry)
    if bn:
        path = os.path.join(folder, bn)
    else:
        path = os.path.join(folder, entry)
    fd = open(path, 'w')
    kid.Template(content, **kwarg).write(file=fd, output=output)
    fd.close()


def extract_pic_js_css(target):
    """Extract the CSS and the Java Script in the target folder"""
    import pygments.formatters
    extract(__name__, 'nosexunit.js', target)
    extract(__name__, 'nosexunit.css', target)
    folder = os.path.join(target, 'images')
    create(folder)
    extract(__name__, 'blank.png', folder, binary=True)
    save(pygments.formatters.HtmlFormatter().get_style_defs('.highlight'), os.path.join(target, 'highlight.css'), binary=False)


def highlight(content):
    """Highlight source code"""
    import pygments, pygments.lexers, pygments.formatters
    lexer = pygments.lexers.PythonLexer()

    class HPyF(pygments.formatters.HtmlFormatter):
        """Class override to avoid &gt; &lt; changing in report"""

        def wrap(self, source, outfile):
            return source

    formatter = HPyF()
    return pygments.highlight(content, lexer, formatter).splitlines()


def exchange(path, data=None):
    """
    Load pickle file if `data` is defined
    Save data if `data` is not defined
    """
    if data is not None:
        fd = open(path, 'wb')
        pickle.dump(data, fd)
        fd.close()
    else:
        if not os.path.exists(path):
            raise nexcepts.ToolError("exchange file doesn't exist: %s" % path)
        fd = open(path, 'rb')
        data = pickle.load(fd)
        fd.close()
        return data
    return


def expand(environ):
    """Expand paths in environment variables"""
    set = False
    path = os.path.dirname(os.path.dirname(os.path.abspath(nosexunit.__file__)))
    for entry in environ.keys():
        if entry.lower().strip() in ('path', 'ld_library_path', 'libpath', 'shlib_path',
                                     'pythonpath'):
            sections = environ[entry].split(os.pathsep)
            atarashii = []
            for section in sections:
                if not on_posix():
                    section = section.replace('"', '')
                section = section.strip()
                if section != '':
                    atarashii.append(os.path.abspath(section))

            if entry.lower().strip() == 'pythonpath':
                atarashii.append(path)
                set = True
            environ[entry] = os.pathsep.join(atarashii)

    if not set:
        environ['PYTHONPATH'] = path
    return environ