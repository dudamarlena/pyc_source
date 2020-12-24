# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboclearsilver/clearsilver.py
# Compiled at: 2006-03-17 00:53:32


class TurboClearsilverError(StandardError):
    __module__ = __name__


class HDFWrapper:
    """
    Convenience layer on top of the low-level ClearSilver python bindings
    for HDF manipulation. This class makes the HDF look and behave more
    like a standard Python dict.

    >>> hdf = HDFWrapper()
    >>> hdf['trac.url'] = 'http://projects.edgewall.com/trac/'
    >>> hdf['trac.version'] = '1.0'
    >>> print hdf
    trac {
      url = http://projects.edgewall.com/trac/
      version = 1.0
    }

    HDFWrapper can also assign Python lists and dicts to HDF nodes,
    automatically expanding them into the corresponding HDF structure.

    A dictionary is mapped to a HDF node with named children:

    >>> hdf = HDFWrapper()
    >>> hdf['item'] = {'name': 'An item', 'value': '0'}
    >>> print hdf
    item {
      name = An item
      value = 0
    }

    A sequence is mapped to a HDF node with children whose names are
    the indexes of the elements:

    >>> hdf = HDFWrapper()
    >>> hdf['items'] = ['Item 1', 'Item 2']
    >>> print hdf
    items {
      0 = Item 1
      1 = Item 2
    }

    Simple values can also be easily retrieved using the same syntax.

    >>> hdf = HDFWrapper()
    >>> hdf['time'] = 42
    >>> hdf['time']
    '42'
    >>> hdf['name'] = 'Foo'
    >>> hdf['name']
    'Foo'

    An attempt to retrieve a value that hasn't been set will raise a KeyError,
    just like a standard dictionary:

    >>> hdf['undef']
    Traceback (most recent call last):
        ...
    KeyError: 'undef'
    
    It may be preferable to return a default value if the given key does not exit.
    It will return 'None' when the specified key is not present:

    >>> hdf.get('time')
    '42'
    >>> hdf.get('undef')

    A second argument may be passed to specify the default return value:

    >>> hdf.get('time', 'Undefined Key')
    '42'
    >>> hdf.get('undef', 'Undefined Key')
    'Undefined Key'

    The 'in' and 'not in' operators can be used to test whether the HDF contains
    a value with a given name.

    >>> 'name' in hdf
    True
    >>> 'undef' in hdf
    False

    has_key() performs the same function:

    >>> hdf.has_key('name')
    True
    >>> hdf.has_key('undef')
    False
    """
    __module__ = __name__

    def __init__(self, loadpaths=[]):
        """Create a new HDF dataset.
        
        The loadpaths parameter can be used to specify a sequence of paths under
        which ClearSilver will search for template files:

        >>> hdf = HDFWrapper(loadpaths=['/etc/templates',
        ...                             '/home/john/templates'])
        >>> print hdf
        hdf {
          loadpaths {
            0 = /etc/templates
            1 = /home/john/templates
          }
        }
        """
        try:
            import neo_cgi
            neo_cgi.update()
            import neo_util
            self.hdf = neo_util.HDF()
        except ImportError, e:
            raise TurboClearsilverError, 'ClearSilver not installed (%s)' % e

        self['hdf.loadpaths'] = loadpaths

    def __getattr__(self, name):
        return getattr(self.hdf, name)

    def __contains__(self, name):
        return self.hdf.getObj(str(name)) != None

    has_key = __contains__

    def get(self, name, default=None):
        value = self.hdf.getValue(str(name), '<<NONE>>')
        if value == '<<NONE>>':
            return default
        return value

    def __getitem__(self, name):
        value = self.get(name, None)
        if value == None:
            raise KeyError, name
        return value

    def __setitem__(self, name, value):
        """Add data to the HDF dataset.
        
        The `name` parameter is the path of the node in dotted syntax. The
        `value` parameter can be a simple value such as a string or number, but
        also data structures such as dicts and lists.

        >>> hdf = HDFWrapper()

        Adding a simple value results in that value being inserted into the HDF
        after being converted to a string.

        >>> hdf['test.num'] = 42
        >>> hdf['test.num']
        '42'
        >>> hdf['test.str'] = 'foo'
        >>> hdf['test.str']
        'foo'

        The boolean literals `True` and `False` are converted to there integer
        representation before being added:

        >>> hdf['test.true'] = True
        >>> hdf['test.true']
        '1'
        >>> hdf['test.false'] = False
        >>> hdf['test.false']
        '0'

        If value is `None`, nothing is added to the HDF:

        >>> hdf['test.true'] = None
        >>> hdf['test.none']
        Traceback (most recent call last):
            ...
        KeyError: 'test.none'
        """
        self.set_value(name, value, True)

    def set_unescaped(self, name, value):
        """
        Add data to the HDF dataset.
        
        This method works the same way as `__setitem__` except that `value`
        is not escaped if it is a string.
        """
        self.set_value(name, value, False)

    def set_value(self, name, value, escape=True):
        """
        Add data to the HDF dataset.
        """

        def add_value(prefix, value):
            if value is None:
                return
            elif value in (True, False):
                self.hdf.setValue(prefix, str(int(value)))
            elif isinstance(value, (str, unicode)):
                self.hdf.setValue(prefix, value)
            elif isinstance(value, dict):
                for k in value.keys():
                    add_value('%s.%s' % (prefix, k), value[k])

            elif hasattr(value, '__iter__') or isinstance(value, (list, tuple)):
                for (idx, item) in enumerate(value):
                    add_value('%s.%d' % (prefix, idx), item)

            else:
                self.hdf.setValue(prefix, str(value))
            return

        add_value(name, value)

    def __str__(self):
        from StringIO import StringIO
        buf = StringIO()

        def hdf_tree_walk(node, prefix=''):
            while node:
                name = node.name() or ''
                buf.write('%s%s' % (prefix, name))
                value = node.value()
                if value or not node.child():
                    if value.find('\n') == -1:
                        buf.write(' = %s' % value)
                    else:
                        buf.write(' = << EOM\n%s\nEOM' % value)
                if node.child():
                    buf.write(' {\n')
                    hdf_tree_walk(node.child(), prefix + '  ')
                    buf.write('%s}\n' % prefix)
                else:
                    buf.write('\n')
                node = node.next()

        hdf_tree_walk(self.hdf.child())
        return buf.getvalue().strip()

    def parse(self, string):
        """Parse the given string as template text, and returns a neo_cs.CS
        object.
        """
        import neo_cs
        cs = neo_cs.CS(self.hdf)
        cs.parseStr(string)
        return cs

    def render(self, template):
        """Render the HDF using the given template.

        The template parameter can be either an already parse neo_cs.CS
        object, or a string. In the latter case it is interpreted as name of the
        template file.
        """
        if isinstance(template, (str, unicode)):
            filename = template
            import neo_cs
            template = neo_cs.CS(self.hdf)
            template.parseFile(filename)
        return template.render()


if __name__ == '__main__':
    import doctest, sys
    doctest.testmod(sys.modules[__name__])