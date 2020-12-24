# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Seth/Programming/input_reader/input_reader/input_reader.py
# Compiled at: 2014-03-01 14:21:20
from __future__ import division, print_function, unicode_literals
from .key_adder import _KeyAdder
from .helpers import ReaderError, SUPPRESS
from .py23compat import py23_basestring
__all__ = [
 b'InputReader', b'ReaderError', b'SUPPRESS']

class InputReader(_KeyAdder):
    """    :py:class:`InputReader` is a class that is designed to read in
    an input file and return the information contained based on rules
    supplied to the class using a syntax similar to what is used in
    the :py:mod:`argparse` module in the Python standard library.

    :py:class:`InputReader` accepts blocks-type, line-type and
    boolean-type keys, mutually exclusive groups, required keys,
    defaults, and more.

    :keyword comment:
        Defines what is a comment in the input block.
        This can be a single string or a list of strings.
        The default is :py:const:`['#']`.  Optional.
    :type comment: str or list
    :keyword case:
        Tells if the keys are case-sensitive or not.
        The default is :py:obj:`False`.  Optional.
    :type case: bool
    :keyword ignoreunknown:
        Ignore keys that are not defined.  The default is
        :py:obj:`False`.  Optional
    :type ignoreunknown: bool
    :keyword default:
        The default default that will be given when a
        key is created without a default.  Optional
    """

    def __init__(self, comment=[
 b'#'], case=False, ignoreunknown=False, default=None):
        """Initiallize the :py:class:`InputReader` class."""
        super(InputReader, self).__init__(case=case)
        self.name = b'main'
        if isinstance(comment, py23_basestring):
            comment = [
             comment]
        self._comment = comment
        try:
            for x in self._comment:
                if not isinstance(x, py23_basestring):
                    raise ValueError(b'comment value must be a str, given ' + repr(x))

        except TypeError:
            raise ValueError(b'comment value must be a str, given ' + repr(self._comment))

        self._ignoreunknown = ignoreunknown
        if not isinstance(self._ignoreunknown, bool):
            raise ValueError(b'ignoreunknown value must be a bool, given ' + repr(self._ignoreunknown))
        self._default = default

    def read_input(self, filename):
        """        Reads in the input from a given file using the supplied rules.

        :argument filename:
            The name of the file to read in, :py:mod:`StringIO` of input,
            or list of strings containing the input itself.
        :rtype: :py:class:`Namespace`: This class contains the read-in data
            each key is stored as members of the class.
        :exception:
            :py:exc:`ReaderError`: Any known errors will be raised with
            this custom exception.
        """
        f = self._read_in_file(filename)
        i, namespace = self._parse_key_level(f, 0)
        self.input_file = f
        self.filename = filename
        self.post_process(namespace)
        return namespace

    def post_process(self, namespace):
        """        Perform post-processing of the data collected from the input file.

        This is a "virtual" method... does nothing and is intended to be
        re-implemented in a subclass.
        """
        pass

    def _read_in_file(self, filename):
        """Store the filename as a list"""
        f = []
        try:
            fl = [ x.rstrip() for x in open(filename) ]
        except (IOError, OSError) as e:
            raise ReaderError(b'Cannot read in file "' + filename + b'":' + str(e))
        except TypeError:
            try:
                fl = filename.getvalue().split(b'\n')
            except AttributeError:
                try:
                    fl = [ x.rstrip() for x in filename ]
                except AttributeError:
                    raise ValueError(b'Unknown object passed to read_input: ' + repr(filename))

        for line in fl:
            for com in self._comment:
                if com in line:
                    line = line.partition(com)[0]

            f.append(line.strip())

        return f