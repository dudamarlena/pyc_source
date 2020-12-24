# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/utils.py
# Compiled at: 2013-03-05 21:43:25
import os, shutil, hashlib, base64, codecs, errno, logging, mimetypes
from fnmatch import fnmatch
from _abcoll import MutableMapping
from weakref import proxy as _proxy
from glob import glob
from tempfile import mkstemp, gettempdir
from subprocess import Popen, PIPE
try:
    import murmur
    has_murmur = True
except:
    has_murmur = False

__all__ = [
 'ordinal_suffix', 'datetimeformat', 'walk_ignore', 'get_hash_from_path',
 'equivalent_files', 'copy_file', 'partition',
 'OrderedDict',
 'render_latex_to_image', 'embed_image']

def ordinal_suffix(day):
    """
    Return the day with the ordinal suffix appended.

    Example: 1st, 2nd, 3rd, 4th, ...
    """
    day = int(day)
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = [
         'st', 'nd', 'rd'][(day % 10 - 1)]
    return '%s%s' % (day, suffix)


def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    """
    Return a formatted time string.

    Keyword arguments:
    value -- tuple or struct_time representing a time
    format -- the desired format
    """
    return value.strftime(format)


if os.name == 'nt':
    import ctypes

    def CreateHardLinkWin(src, dst):
        if not ctypes.windll.kernel32.CreateHardLinkA(dst, src, 0):
            raise OSError


    os.link = CreateHardLinkWin

def walk_ignore(path):
    """Custom walker that ignores specific filenames"""
    ignores = ('.*', '*~', '#*', '_*')
    for dirpath, dirnames, filenames in os.walk(path):
        for pattern in ignores:
            filenames[:] = [ n for n in filenames if not fnmatch(n, pattern) ]
            dirnames[:] = [ n for n in dirnames if not fnmatch(n, pattern) ]

        yield (
         dirpath, dirnames, filenames)


def get_hash_from_path(path, algorithm='sha1'):
    """Returns the hash of the file `path`."""
    f = open(path)
    content = f.read()
    f.close()
    m = hashlib.new(algorithm)
    m.update(content)
    return m.hexdigest()


def equivalent_files(src, dst):
    """True if `src` and `dst` are the equivalent."""
    src_stat, dst_stat = os.stat(src), os.stat(dst)
    if src_stat.st_dev == dst_stat.st_dev and src_stat.st_ino == dst_stat.st_ino:
        return True
    else:
        file_hash = murmur.file_hash if has_murmur else get_hash_from_path
        return file_hash(src) == file_hash(dst)


def copy_file(src, dst, hardlinks=False):
    """
    Copy `src` to `dst`.

    The parent directories for `dst` are created.

    To increase performance, this function will check if the file `dst`
    exists and compare the hash of `src` and `dst`. The file will
    only be copied if the hashes differ.

    If `hardlinks` is true, instead of copying hardlinks will be created
    if possible.
    """
    try:
        os.makedirs(os.path.dirname(dst))
    except OSError:
        pass

    if os.path.isfile(dst):
        if equivalent_files(src, dst):
            return False
    try:
        if hardlinks:
            try:
                os.link(src, dst)
                return True
            except OSError:
                logging.debug("Could not create hardlink for '%s'->'%s'.", src, dst)

        shutil.copy2(src, dst)
        return True
    except IOError:
        logging.debug("Caught IOError when copying '%s'->'%s'.", src, dst)


def partition(alist, indices):
    """Splits at the given indices.

    >>> partition('crocodile', [4, 5])
    ['croc', 'o', 'dile']
    """
    return [ alist[i:j] for i, j in zip([0] + indices, indices + [None]) ]


class _Link(object):
    __slots__ = ('prev', 'next', 'key', '__weakref__')


class OrderedDict(dict, MutableMapping):
    """Dictionary that remembers insertion order"""

    def __init__(self, *args, **kwds):
        """Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        """
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = _Link()
            root.prev = root.next = root
            self.__map = {}

        self.update(*args, **kwds)

    def clear(self):
        """od.clear() -> None.  Remove all items from od."""
        root = self.__root
        root.prev = root.next = root
        self.__map.clear()
        dict.clear(self)

    def __setitem__(self, key, value):
        """od.__setitem__(i, y) <==> od[i]=y"""
        if key not in self:
            self.__map[key] = link = _Link()
            root = self.__root
            last = root.prev
            link.prev, link.next, link.key = last, root, key
            last.next = root.prev = _proxy(link)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        """od.__delitem__(y) <==> del od[y]"""
        dict.__delitem__(self, key)
        link = self.__map.pop(key)
        link.prev.next = link.next
        link.next.prev = link.prev

    def __iter__(self):
        """od.__iter__() <==> iter(od)"""
        root = self.__root
        curr = root.next
        while curr is not root:
            yield curr.key
            curr = curr.next

    def __reversed__(self):
        """od.__reversed__() <==> reversed(od)"""
        root = self.__root
        curr = root.prev
        while curr is not root:
            yield curr.key
            curr = curr.prev

    def __reduce__(self):
        """Return state information for pickling"""
        items = [ [k, self[k]] for k in self ]
        tmp = (
         self.__map, self.__root)
        del self.__map
        del self.__root
        inst_dict = vars(self).copy()
        self.__map, self.__root = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return (
         self.__class__, (items,))

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update
    pop = MutableMapping.pop
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items
    iterkeys = MutableMapping.iterkeys
    itervalues = MutableMapping.itervalues
    iteritems = MutableMapping.iteritems
    __ne__ = MutableMapping.__ne__

    def popitem(self, last=True):
        """od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        """
        if not self:
            raise KeyError('dictionary is empty')
        key = next(reversed(self) if last else iter(self))
        value = self.pop(key)
        return (key, value)

    def __repr__(self):
        """od.__repr__() <==> repr(od)"""
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items())

    def copy(self):
        """od.copy() -> a shallow copy of od"""
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        """
        d = cls()
        for key in iterable:
            d[key] = value

        return d

    def __eq__(self, other):
        """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        """
        if isinstance(other, OrderedDict):
            return len(self) == len(other) and all(_imap(_eq, self.iteritems(), other.iteritems()))
        return dict.__eq__(self, other)


DOC_HEAD = '\n\\documentclass[12pt]{article}\n\\usepackage[utf8x]{inputenc}\n\\usepackage{amsmath}\n\\usepackage{amsthm}\n\\usepackage{amssymb}\n\\usepackage{amsfonts}\n\\usepackage{bm}\n\\pagestyle{empty}\n'
DOC_BODY = '\n\\begin{document}\n%s\n\\end{document}\n'

def render_latex_to_image(math):
    """
    Renders the given formula (in LaTeX markup) to an image.
    """
    latex = DOC_HEAD + DOC_BODY % math
    latex_fd, latex_filename = mkstemp(suffix='.tex')
    with codecs.open(latex_filename, 'w', 'utf-8') as (latex_file):
        latex_file.write(latex)
    latex_cmdline = [
     'latex', '--interaction=nonstopmode', latex_filename]
    dvipng_cmdline = [
     'dvipng',
     '-o', latex_filename.replace('.tex', '.png'),
     '-T', 'tight',
     '-bg', 'Transparent',
     '-z9',
     latex_filename.replace('.tex', '.dvi')]
    curdir = os.getcwd()
    os.chdir(gettempdir())
    try:
        for cmdline, cmdref in [(latex_cmdline, 'LaTeX'), (dvipng_cmdline, 'dvipng')]:
            try:
                p = Popen(cmdline, stdout=PIPE, stderr=PIPE)
            except OSError as err:
                if err.errno != errno.ENOENT:
                    raise
                logging.error('%s command cannot be run, but is needed for math markup.', cmdref)
                return

            stdout, stderr = p.communicate()
            if p.returncode != 0:
                logging.error('%s command exited with error: \n[stderr]\n%s\n[stdout]\n%s', cmdref, stderr, stdout)
                return

    finally:
        for filename in glob(latex_filename[0:-4] + '*'):
            if not filename.endswith('.png'):
                os.remove(filename)

        os.chdir(curdir)

    return latex_filename.replace('.tex', '.png')


def embed_image(image_path):
    """
    Returns a Data URI string of the image for embedding in HTML or CSS.
    """
    mimetype = mimetypes.guess_type(image_path)[0]
    b64img = base64.encodestring(open(image_path, 'rb').read()).replace('\n', '')
    return ('').join(['data:', mimetype, ';base64,', b64img])