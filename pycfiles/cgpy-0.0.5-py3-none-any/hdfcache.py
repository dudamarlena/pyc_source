# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\utils\hdfcache.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = '\nFunction decorator to log/cache input/output recarrays to HDF group of tables\n\nGiven a function func(input) -> output whose input and output are numpy record \narrays, so that input.dtype.names and output.dtype.names are not None.\n\nThis module provides a way to automatically store input and output to \nHDF tables, using the dtype as table descriptors. Previously computed outputs \nare looked up rather than recomputed. Lookup is based on a the built-in hash()\napplied to autoname(input).data\nGael Varoquaux\' joblib offers another, slower, hash for Numpy arrays, which is \nprobably not needed for our purposes.\nhttps://launchpad.net/joblib\n\nSeveral functions can be cached to the same HDF file. To achieve this, the \ndecorator is a method of an object that owns the file. (This design is borrowed \nfrom Gael Varoquaux\'s "joblib" package, https://launchpad.net/joblib.)\n\n@todo: log process id or job id\n@todo: Allow read-only opening of a cache. This would require parsing options \nat the start of the module.\n@todo: Use temp file for doctests by default, simplifying the following code: \n\nAn example follows, using a temporary file by default. If you\'d like to inspect \nthe HDF output, you can specify a filename by passing a --filename option when \nrunning the doctests.\n\n>>> try:\n...     filename = options.filename\n... except NameError:\n...     filename = None\n>>> if filename is None:\n...     import tempfile\n...     filename = os.path.join(tempfile.mkdtemp(), \'cachetest.h5\')\n\nFirst, create an Hdfcache instance.\n\n>>> hdfcache = Hdfcache(filename)\n\nNow its method hdfcache.cache(func) can be used as a decorator:\n\n>>> @hdfcache.cache\n... def f(x, a, b=10):\n...     "This is the docstring for function f"\n...     result = np.zeros(1, dtype=[("y", float)])\n...     result["y"] = x["i"] * 2 + x["f"] + a * b\n...     print "Evaluating f:", x, a, b, "=>", result\n...     return result\n\nCalling hdfcache.cache again will cache multiple functions in the same HDF file.\n\n>>> @hdfcache.cache\n... def g(y):\n...     "This is the docstring for the function g"\n...     result = np.zeros(1, \n...         dtype=[("a", np.int32), ("b", float), ("c", complex)])\n...     result["a"] = int(y["y"])\n...     result["b"] = 1 / y["y"]\n...     result["c"] = complex(0, y["y"])\n...     print "Evaluating g:", y, "=>", result\n...     return result\n\nThe function is evaluated normally the first time an input is encountered.\n\n>>> x = np.rec.fromarrays([[1, 2], [1.25, 3.5]], \n...     dtype=[("i", np.int32), ("f", float)])\n>>> np.concatenate([g(f(xi, 5)) for xi in x])\nEvaluating f: [(1, 1.25)] 5 10 => [(53.25,)]\nEvaluating g: [(53.25,)] => [(53, 0.0187793..., 53.25j)]\nEvaluating f: [(2, 3.5)] 5 10 => [(57.5,)]\nEvaluating g: [(57.5,)] => [(57, 0.0173913..., 57.5j)]\narray([(53, 0.0187793..., 53.25j),\n       (57, 0.0173913..., 57.5j)],\n      dtype=[(\'a\', \'<i4\'), (\'b\', \'<f8\'), (\'c\', \'<c16\')])\n\nIn addition, the input and output are stored in the HDF file.\n\n>>> print "Cache:", hdfcache.file    # doctest output cannot start with ellipsis\nCache: ...\n/f (Group) \'\'\n/f/hash (Table(2,), shuffle, zlib(1)) \'\'\n/f/input (Table(2,), shuffle, zlib(1)) \'\'\n/f/output (Table(2,), shuffle, zlib(1)) \'\'\n/f/timing (Table(2,), shuffle, zlib(1)) \'\'\n/g (Group) \'\'\n/g/hash (Table(2,), shuffle, zlib(1)) \'\'\n/g/input (Table(2,), shuffle, zlib(1)) \'\'\n/g/output (Table(2,), shuffle, zlib(1)) \'\'\n/g/timing (Table(2,), shuffle, zlib(1)) \'\'\n\nCalling the decorated function again with the same inputs will avoid calling \nthe original function.\n\n>>> f(x[1], 5)\nrec.array([(57.5,)], dtype=[(\'y\', \'<f8\')])\n\nThe source code of a cached function is stored as an attribute of its Group.\n\n>>> print hdfcache.file.root.f._v_attrs.sourcecode   # doctest: +SKIP\n@hdfcache.cache\ndef f(x, a, b=10):...\n>>> hdfcache.file.root.f._v_attrs  # doctest: +SKIP\n/f._v_attrs (AttributeSet),...\n    sourcecode := \'...\',\n    sourcefile := \'<doctest __main__[3]>\']\n\nClosing the HDF file:\nhdfcache.file is a property that will create the file if needed and reopen it \nif it has been closed. Remember to close the file, either explicitly:\n\n>>> hdfcache.file.close()\n>>> hdfcache._file # The Hdfcache\'s internal tables.File instance\n<closed File>\n\nor using a "with" statement:\n\n>>> with hdfcache:\n...     hdfcache.file\nFile(filename=..., title=\'\', mode=\'a\', rootUEP=\'/\', ...\n>>> hdfcache._file\n<closed File>\n\nCompression is enabled by default, but can be disabled by passing filters=None \nto the Hdfcache() constructor.\n\n\n== Comparing hash values manually ==\n\nThe ahash(x) function currently applies the built-in hash() to x.__data__, \nconverting x to a Numpy array if needed. This is fast and tolerant towards \nminor differences in shape and dtype. Just be aware of cases like these, which \nhave the same binary __data__:\n\n>>> ahash(np.zeros(1)) == ahash(np.zeros(8, np.int8))       # float is 8 bytes\nTrue\n\nHere follow some details that are not relevant to the current ahash(), but are \nimportant if you choose a stricter hash function.\n\nNumpy structured arrays and PyTables tables both distinguish between:\n\n>>> type(x[0])\n<class \'numpy.core.records.record\'>\n>>> type(x[0:1])\n<class \'numpy.core.records.recarray\'>\n>>> x[0]\n(1, 1.25)\n>>> x[0:1]\nrec.array([(1, 1.25)], dtype=[(\'i\', \'<i4\'), (\'f\', \'<f8\')])\n\nNote, though, that \n\n>>> x[0].dtype == x[0:1].dtype\nTrue\n\nThese nuances may affect hash values: whether an input is ndarray or recarray, \nits shape and dimensionality.\n\n>>> ahash(x[1]) == ahash(x[1:2]) # False if using joblib.hash as hash\nTrue\n\nThe following is a reliable way to check whether \nthe hash of an input is in an existing hash Table.\nWe are searching for record x[1] in the HDF group hdfcache.file.root.f.\n\n>>> with hdfcache.file as f:\n...     f.root.f.hash.getWhereList("hash == h", dict(h=ahash(autoname(x[1]))))\narray([1]...)\n\nDetails:\n\n>>> h1 = ahash(x[1:2])\n>>> want = dict([("joblib.hash", "4a14c07534c7a24053e58540b74de973"),\n...              ("Windows XP 32-bit", 1710834134),\n...              ("Windows 7 32-bit", 6484299406236008918)])\n>>> h1 in want.values()\nTrue\n>>> with hdfcache:\n...     hash = hdfcache.file.root.f.hash # Table object\n...     h = hash[:] # extract all records as structured ndarray\n>>> want = dict([\n...     ("joblib.hash", np.array([(\'cadf9e2413df9d83e2303522bc1267a9\',), \n...                               (\'4a14c07534c7a24053e58540b74de973\',)], \n...                               dtype=[(\'hash\', \'|S32\')])),\n...     ("Windows XP 32-bit",  np.array([(773416804,), (1710834134,)], \n...                               dtype=[(\'hash\', \'<i4\')])),\n...     ("Windows 7 32-bit", np.array([(-5981222333818771612,), \n...                       (6484299406236008918,)], dtype=[(\'hash\', \'<i8\')]))])\n>>> any([all([(i == j) for i, j in zip(h["hash"], v["hash"])]) \n...     for v in want.values()])\nTrue\n>>> np.where(h1 == h["hash"])\n(array([1]),)\n\nThese are equivalent:\n\n>>> ahash(x[1:2]) == ahash(autoname(x[1]))\nTrue\n\nFor the painful details, see \nhttp://thread.gmane.org/gmane.comp.python.pytables.user/1238/focus=1250\n'
import itertools
from contextlib import nested
from glob import glob
import os
from ..utils.poormanslock import Lock
import shutil, tables as pt, numpy as np
from ..utils.argrec import autoname
import inspect
from functools import wraps
import time, logging
log = logging.getLogger('hdfcache')
log.addHandler(logging.StreamHandler())
fmtstr = '%(' + (')s\t%(').join(('asctime levelname name lineno process message').split()) + ')s'
log.handlers[0].setFormatter(logging.Formatter(fmtstr))

def ahash(x):
    """
    Hash the raw data of a Numpy array
    
    The input will be converted to a Numpy array if possible.    
    The shape and dtype of the array does not enter into the hash.
    
    >>> x = np.arange(5)
    >>> y = np.arange(5)
    >>> ahash(x) == ahash(y) == ahash(range(5))
    True
    """
    x = np.asarray(x)
    x.setflags(write=False)
    return hash(x.data)


class NoHdfcache(object):
    """A caricature of a caching decorator that does not actually cache"""

    def __init__(self, filename):
        """Initialize resources shared among caches"""
        pass

    def cache(self, func):
        """
        A null decorator implemented as an instance method

        >>> nohdfcache = NoHdfcache("dummy.filename")
        >>> @nohdfcache.cache
        ... def f(x): return x * x
        >>> @nohdfcache.cache
        ... def g(y): return y * y * y
        >>> f(2)
        4
        >>> g(3)
        27
        """
        return func


class DictHdfcache(object):
    """Prototype of caching using a shared resource (a dict)"""

    def __init__(self, filename):
        """Initialize a single dict that will hold multiple caches"""
        self.d = {}
        self.argspec = {}
        self.output_type = {}

    def cache(self, func):
        """
        Cache a function, using a resource in scope of an object instance
        
        Note that "self" is in scope of the decorator method, providing access 
        to shared resources. By contrast, the scope of "func" is limited to 
        each decoration. Each decoration involves a single call to cache().
        It initializes any sub-resources specific to "func".
        Finally, it defines the actual wrapper as a plain function, but one 
        whose scope includes both "self" and "func".
        
        Access to "self" preserves information (the cache) between calls to the 
        wrapped function. Because it is a plain function, it can adopt the 
        docstring of func by use of @wraps(func).
        
        Details of the caching can be deferred until the required information 
        is available, like knowing the dtype of an output array before creating 
        a corresponding HDF table.
        
        Verifying what's going on...
        
        >>> dicthdfcache = DictHdfcache("dummy.filename")
        >>> @dicthdfcache.cache
        ... def f(x): return x * x
        cache: initializing resources for a decorated function
        >>> f(2)
        cache: computed f 2 => 4
        cache: deferred initialization
        4
        >>> f(3)
        cache: computed f 3 => 9
        9
        >>> f(3)
        cache: returning cached value
        9
        
        Create another cache using the same resource (a dict); the end result 
        is shown below.
        
        >>> @dicthdfcache.cache
        ... def g(y): return y * y * y
        cache: initializing resources for a decorated function
        >>> g(3)
        cache: computed g 3 => 27
        cache: deferred initialization
        27
        
        Here's the dictionary with the two caches.
        
        >>> srt = sorted(dicthdfcache.d.items(), key=lambda x: x[0].__name__)
        >>> for k, v in srt:
        ...     print k, sorted(v.items(), key=lambda x: x[-1])
        <function f at 0x...> [(..., 4), (..., 9)]
        <function g at 0x...> [(..., 27)]
        
        A function with both required, default, and variable-length unnamed and 
        keyword arguments.
        
        >>> @dicthdfcache.cache
        ... def h(a, b=10, *args, **kwargs): pass
        cache: initializing resources for a decorated function
        
        Here are the argument specifications, which could be used for deferred
        specification of an "args" table.
        
        >>> sorted(dicthdfcache.argspec.items(), key=lambda x: x[0].__name__)
        [(<function f at 0x...>,
          ArgSpec(args=['x'], varargs=None, keywords=None, defaults=None)),
         (<function g at 0x...>,
          ArgSpec(args=['y'], varargs=None, keywords=None, defaults=None)),
         (<function h at 0x...>,
          ArgSpec(args=['a', 'b'], varargs='args', keywords='kwargs', 
          defaults=(10,)))]
        """
        print 'cache: initializing resources for a decorated function'
        self.d[func] = {}
        self.argspec[func] = inspect.getargspec(func)

        @wraps(func)
        def wrapper(input_):
            key = ahash(input_)
            if key in self.d[func]:
                print 'cache: returning cached value'
                return self.d[func][key]
            else:
                output = func(input_)
                print 'cache: computed', func.__name__, input_, '=>', output
                if not self.d[func]:
                    print 'cache: deferred initialization'
                    self.output_type[func] = type(output)
                self.d[func][key] = output
                return output

        return wrapper


class HdfcacheException(Exception):
    """Class for :class:`Hdfcache` exceptions."""


class Hdfcache(object):
    """HDF file wrapper with function caching decorator"""

    def __init__(self, filename, where='/', filters=pt.Filters(complevel=1), mode='a', withflagfile=True, *args, **kwargs):
        """
        Constructor for HDF cache object.
        
        Arguments "filename", "filters", "mode" are passed to Tables.openFile().
        Argument "where" identifies a parent group for all the function caches.
        The boolean argument "withflagfile" says whether to create a flag file 
        with the extension ".delete_me_to_stop" that indicates that the process 
        is running. Deleting or renaming that file will raise an exception at a 
        time when no function is being evaluated, ensuring clean exit and 
        flushing of buffers.
        """
        kwargs['filename'] = filename
        kwargs['mode'] = mode
        kwargs['filters'] = filters
        self._file = None
        self.where = where
        self.fileargs = args
        self.filekwargs = kwargs
        self.withflagfile = withflagfile
        if withflagfile:
            self.flagfilename = filename + '.delete_me_to_stop'
            self.incontext = False
        return

    @property
    def file(self):
        """
        File object for an HDF cache, see Tables.File in PyTables.
        
        The file is created if it doesn't exist, reopened if it has been closed.
        """
        if not (self._file and self._file.isopen):
            self._file = pt.openFile(*self.fileargs, **self.filekwargs)
            log.debug('Opened cache file')
        return self._file

    def group(self, funcname):
        """Dictionary of HDF parent groups for each function."""
        try:
            return self.file.getNode(self.where, funcname)
        except pt.NoSuchNodeError:
            return self.file.createGroup(self.where, funcname, createparents=True)

    def __enter__(self):
        """
        Enter the context of a with statement, optionally creating flag file.
        
        This doctest tests the flag file functionality. The flag file is 
        deleted on the first pass through the function, causing an 
        exception to be raised.
        
        >>> import tempfile, shutil, os
        >>> dtemp = tempfile.mkdtemp()
        >>> filename = os.path.join(dtemp, 'entertest.h5')
        >>> cacher = Hdfcache(filename)
        >>> @cacher.cache
        ... def f(x):
        ...     os.remove(cacher.flagfilename)
        ...     return x
        >>> with cacher:
        ...     while True:
        ...         y = f(0)
        Traceback (most recent call last):
        HdfcacheException: Flag file not found when calling <function f...
        """
        if self.withflagfile:
            self.incontext = True
            open(self.flagfilename, 'w').close()
        return self

    def __exit__(self, type_, value, tb):
        """
        Exit context of with statement, closing file and removing any flag file.
        """
        if self._file and self._file.isopen:
            self.file.close()
        if self.withflagfile and os.path.exists(self.flagfilename):
            self.incontext = False
            os.remove(self.flagfilename)

    def cache(self, func):
        """
        Decorator for function-specific caching of inputs and outputs
        
        This gets called once for each function being decorated, creating a 
        new scope with HDF node objects specific to the decorated function.
        
        The Group object of the decorated function will currently not survive 
        after the first with statement, because the File is closed and the 
        node initialization code is never called again. I'll need to either put 
        all of the "open if exist else create" stuff in the wrapper below, or 
        encapsulate that into a separate object, which has to know about both 
        file (in the scope of the "hdfcache" instance) and 
        func (in the scope of the "cache" function).
        
        How to tell if a node is closed: _v_isopen
        Natural naming will open if required, so just need the group and always 
        be explicit about group.hash, group.input, group.output.
        
        @todo: make iterator that buffers hashes so we can read many at a time 
        using table.itersequence, see: 
        http://wiki.umb.no/CompBio/index.php/HDF5_in_Matlab_and_Python
        """
        funcname = func.__name__
        group = self.group(funcname)
        self.set_source_attr(group, func)
        hashdict = dict(uninitialized=True)

        @wraps(func)
        def wrapper(input_, *args, **kwargs):
            if self.withflagfile and self.incontext:
                if not os.path.exists(self.flagfilename):
                    msg = 'Flag file not found when calling %s'
                    raise HdfcacheException(msg % func)
            input_ = autoname(input_)
            ihash = ahash(input_)
            group = self.group(funcname)
            if 'uninitialized' in hashdict:
                try:
                    hash_ = group.hash
                    log.debug('Reading existing hashes')
                    hashdict.update((h, i) for i, (h,) in enumerate(hash_[:]))
                except pt.NoSuchNodeError:
                    log.debug('Creating hash table for %s', func)
                    hashdescr = autoname(ihash)[:0]
                    hashdescr.dtype.names = ['hash']
                    hash_ = self.file.createTable(group, 'hash', hashdescr)
                    self.set_source_attr(hash_, ahash)

                del hashdict['uninitialized']
            if ihash in hashdict:
                log.debug('Cache hit %s: %s %s', func, ihash, input_)
                return autoname(group.output[hashdict[ihash]])
            else:
                log.debug('Cache miss %s: %s %s', func, ihash, input_)
                timing = np.rec.fromarrays([[0.0], [0.0], [0.0]], names=[
                 'seconds', 'start', 'end'])
                timing.start = time.clock()
                output = autoname(func(input_, *args, **kwargs))
                timing.end = time.clock()
                timing.seconds = timing.end - timing.start
                if hashdict:
                    hash_ = group.hash
                    log.debug('Appending to input, output, and timing tables')
                    group.input.append(input_)
                    group.output.append(output)
                    group.timing.append(timing)
                else:
                    log.debug('Creating input, output, and timing tables')
                    self.file.createTable(group, 'input', input_)
                    self.file.createTable(group, 'output', output)
                    self.file.createTable(group, 'timing', timing)
                hashdict[ihash] = hash_.nrows
                hash_.append(autoname(ihash))
                return output

        self.file.close()
        return wrapper

    @staticmethod
    def set_source_attr(node, obj):
        """Store the source code of an object as an attribute of an HDF node."""
        if 'sourcecode' not in node._v_attrs:
            try:
                node._v_attrs.sourcefile = inspect.getfile(obj)
                node._v_attrs.sourcecode = inspect.getsource(obj)
            except (TypeError, IOError):
                node._v_attrs.sourcefile = 'built-in'
                node._v_attrs.sourcecode = ''


def hdfcat(pathname='*.h5', outfilename='concatenated.h5'):
    """
    Concatenate data scattered over many HDF files with equal layout.
    
    All HDF files matching pathname are concatenated into a new file denoted by 
    outfilename. If the output file already exists, no action is taken. The 
    function returns True if the output file was created and False otherwise.
    A lock is held while concatenating, so that work can be shared between 
    multiple instances of a script (see the "grabcounter" module), while only 
    one instance concatenates the results.
    
    Compression settings are inherited from the biggest file.
    
    NOTE: NEED TO ENSURE THAT ALL PROCESSES HAVE FINISHED FLUSHING HDF BUFFERS 
    BEFORE CONCATENATING. See grabcounter.grabsummer().
    
    The use of iterators conserves memory, so this should work for arbitrarily 
    large data sets. It is also quite IO-efficient due to PyTables' buffering 
    of Table objects. The only limitation is perhaps that we need simultaneous 
    handles to all input files. Also, this currently only concatenates tables, 
    not arrays. (It might work out of the box, at least for VLArray.)
    
    Todo: Guard against adopting the structure of an unpopulated cache file 
    left by job instances that arrived too late to do any work. Currently I use 
    the biggest file and hope that's okay.
    
    Adapted from http://cilit.umb.no/WebSVN/wsvn/Cigene_Repository/CigeneCode/CompBio/cGPsandbox/h5merge.py
    
    The following doctests are more for testing than documentation.
    
    Distribute sample data over three HDF files in a temporary directory.
    
    >>> import tempfile
    >>> filename = os.path.join(tempfile.mkdtemp(), 'cachetest.h5')
    >>> a = np.rec.fromarrays([[0, 2, 1]], names="a")
    >>> b = np.rec.fromarrays([[11, 12, 10]], names="b")
    >>> def writedata(i):
    ...     with pt.openFile("%s.%s.h5" % (filename, i), "w") as f:
    ...         f.createTable(f.root, "a", a[i:i+1])
    ...         f.createTable("/group1", "b", b[i:i+1], createparents=True)
    ...         return str(f.root.a[:]) + " " + str(f.root.group1.b[:]) + " " + str(f)
    >>> for i in 0, 1, 2:
    ...     print "Part", i, writedata(i)
    Part 0 [(0,)] [(11,)] ...cachetest.h5.0.h5...
    / (RootGroup) ''
    /a (Table(1,)) ''
    /group1 (Group) ''
    /group1/b (Table(1,)) ''
    Part 1 [(2,)] [(12,)] ...cachetest.h5.1.h5...
    / (RootGroup) ''
    /a (Table(1,)) ''
    /group1 (Group) ''
    /group1/b (Table(1,)) ''
    Part 2 [(1,)] [(10,)] ...cachetest.h5.2.h5...
    / (RootGroup) ''
    /a (Table(1,)) ''
    /group1 (Group) ''
    /group1/b (Table(1,)) ''

    Part 0 [(0, 11)] ...cachetest.h5.0.h5...
    / (RootGroup) ''
    /data (Table(1,)) ''
    /group1 (Group) ''
    /group1/data (Table(1,)) ''
    Part 1 [(2, 12)] ...cachetest.h5.1.h5...
    / (RootGroup) ''
    /data (Table(1,)) ''
    /group1 (Group) ''
    /group1/data (Table(1,)) ''
    Part 2 [(1, 10)] ...cachetest.h5.2.h5...
    / (RootGroup) ''
    /data (Table(1,)) ''
    /group1 (Group) ''
    /group1/data (Table(1,)) ''
    
    Concatenate them together. (Note: The output is not sorted.)
    
    >>> hdfcat(filename + ".*.h5", filename + ".concatenated")
    True
    >>> with pt.openFile(filename + ".concatenated") as f:
    ...     print "Concatenated", str(f)
    Concatenated ...cachetest.h5.concatenated...
    / (RootGroup) ''
    /a (Table(3,)) ''
    /group1 (Group) ''
    /group1/b (Table(3,)) ''
    >>> with pt.openFile(filename + ".concatenated") as f:
    ...     np.testing.assert_equal(sorted(f.root.a.cols.a), (0, 1, 2))
    ...     np.testing.assert_equal(sorted(f.root.group1.b.cols.b), (10, 11, 12))

    False is returned if the output file already exists.
    
    >>> hdfcat(filename + ".*.h5", filename + ".concatenated")
    False
    """
    try:
        with Lock(outfilename + '.lock'):
            if os.path.exists(outfilename):
                return False
            infilenames = glob(pathname)
            infilenames.sort(key=os.path.getsize)
            bigfilename = infilenames.pop()
            with nested(*(pt.openFile(i) for i in infilenames)) as (fin):
                shutil.copy(bigfilename, outfilename)
                with pt.openFile(outfilename, 'a') as (fout):

                    def tablewalkers(f):
                        """List of iterators over nodes of HDF files."""
                        return [ fi.walkNodes(classname='Table') for fi in f ]

                    for t in itertools.izip_longest(*tablewalkers(fin)):
                        pass

                    fin = [ fi for fi, ti in zip(fin, t) if ti ]
                    for t in itertools.izip(*tablewalkers([fout] + fin)):
                        tout, tin = t[0], t[1:]
                        for ti in tin:
                            tout.append(ti[:])

        return True
    except IOError as exc:
        if 'Timed out' in str(exc):
            return False
        raise


if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser()
    parser.add_option('-o', '--filename', help='Name of output HDF5 file')
    parser.add_option('-v', '--verbose', action='store_true', help='Run doctests with verbose output')
    parser.add_option('--debug', action='store_true', help='Turn on debug logging for HDF cache')
    options, _args = parser.parse_args()
    if options.debug:
        log.setLevel(logging.DEBUG)
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)