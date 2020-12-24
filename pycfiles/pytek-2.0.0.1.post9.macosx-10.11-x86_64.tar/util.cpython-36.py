# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/pytek/util.py
# Compiled at: 2018-02-24 21:29:12
# Size of source mod 2**32: 27853 bytes
import re, os

class Configurator(object):
    __doc__ = '\n    The `Configurator` class creates helper objects that can be used\n    to easily add methods to a class to configure and query a particular setting\n    on the device.\n\n    The easiest way to understand it is by example. First, a stripped down usage example:\n\n\n    .. code :: python\n\n        class MyDevice(object):\n\n            __metaclass__ = Configurator.ConfigurableMeta\n\n            @Configurator.config("FOO:BAR")\n            def foobar(self, val):\n                return val.lower()\n\n            @foobar.setter\n            def foobar(self, val):\n                return val.upper()\n\n\n            @Configurator.config\n            def frobbed(self, val):\n                return (val == "ON")\n\n            @frobbed.setter\n            def frobbed(self, val):\n                return "ON" if val else "OFF"\n\n\n    And now, a more thorough example, expanded from this:\n\n    .. code :: python\n\n        class MyDevice(object):\n\n            #Make sure it uses the ConfigurableMeta class as its metaclass,\n            # so Configurator objects in the class definition get replaced with\n            # appropriate methods.\n            __metaclass__ = Configurator.ConfigurableMeta\n\n            #Just some ordinary instance attributes, which we will be the target of\n            # our setting configuring and querying.\n            __foobar = "TAZ"\n            __frobbed = "OFF"\n\n            #This is where the class actually implements sending command and queries.\n            # The Configurator objects will call these methods.\n\n            def send_command(self, name, arg):\n                print "~~~> %s %s" % (name, arg)\n                if name == "FOO:BAR":\n                    if not isinstance(arg, str):\n                        raise TypeError()\n                    if arg != arg.upper():\n                        raise ValueError()\n                    self.__foobar = arg\n\n                elif name == "FROBBED":\n                    if arg not in ("ON", "OFF"):\n                        raise ValueError()\n                    self.__frobbed = arg\n\n                else:\n                    raise KeyError()\n\n\n            def send_query(self, name):\n                print "???? %s" % name\n                if name == "FOO:BAR":\n                    val = self.__foobar\n                elif name == "FROBBED":\n                    val = self.__frobbed\n                else:\n                    raise KeyError()\n                print "    <<<< %s" % val\n                return val\n\n\n            #Now, define Configurators for each of our configurable settings.\n\n\n            #First, for the FOO:BAR setting, which will be accessed through a\n            # function called `foobar`.\n\n            @Configurator.config("FOO:BAR")\n            def foobar(self, val):\n                #Translate a value returned by `send_query` into a value to return\n                # to the calling code.\n                return val.lower()\n\n            @foobar.setter\n            def foobar(self, val):\n                #Translate a value provided by the calling code into a value that\n                # will be passed to `send_command`.\n                return val.upper()\n\n\n            #Now, the FROBBED setting. We can use implicit named in the decorator\n            # for this one.\n\n            @Configurator.config\n            def frobbed(self, val):\n                \'\'\'\n                +++\n                Querying returns True for "ON", and False for "OFF".\n                \'\'\'\n                if val == "ON":\n                    return True\n                if val == "OFF":\n                    return False\n                raise ValueError(val)\n\n            @frobbed.setter\n            def frobbed(self, val):\n                \'\'\'\n                +++\n                Valid values for configuring are True and False, or synonomously\n                "ON" and "OFF".\n                \'\'\'\n                if val is True or val == "ON":\n                    return "ON"\n                elif val is False or val == "OFF":\n                    return "OFF"\n                raise ValueError()\n\n\n    With the above code, you could then do the following:\n\n    .. code :: pycon\n\n        >>> dev = MyDevice()\n        >>> dev.foobar()\n        ???? FOO:BAR\n            <<<< TAZ\n        \'taz\'\n        >>>\n        >>> dev.foobar(\'razzle-dazzle\')\n        ~~~> FOO:BAR RAZZLE-DAZZLE\n        >>>\n        >>> dev.foobar()\n        ???? FOO:BAR\n            <<<< RAZZLE-DAZZLE\n        \'razzle-dazzle\'\n        >>>\n        >>>\n        >>> dev.frobbed()\n        ???? FROBBED\n            <<<< OFF\n        False\n        >>> dev.frobbed(True)\n        ~~~> FROBBED ON\n        >>> dev.frobbed()\n        ???? FROBBED\n            <<<< ON\n        True\n        >>>\n        >>> dev.frobbed(False)\n        ~~~> FROBBED OFF\n        >>> dev.frobbed()\n        ???? FROBBED\n            <<<< OFF\n        False\n        >>>\n        >>> dev.frobbed("ON")\n        ~~~> FROBBED ON\n        >>> dev.frobbed()\n        ???? FROBBED\n            <<<< ON\n        True\n        >>>\n        >>> dev.frobbed("???")\n        Traceback (most recent call last):\n          File "<stdin>", line 1, in <module>\n          File "src\\pytek\\util.py", line 125, in config\n            return self(device, val)\n          File "src\\pytek\\util.py", line 116, in __call__\n            self.configure(device, self.name, self.set(device, val))\n          File "temp.py", line 94, in frobbed\n            raise ValueError()\n        ValueError\n        >>>\n        >>>\n        >>> help(dev.foobar)\n        Help on method foobar in module pytek.util:\n\n        foobar(device, val=None) method of temp.MyDevice instance\n            Configures or queries the value of the ``FOO:BAR`` setting on the device.\n            If a value is given, then the setting is configured to the given value.\n            If the value is `None` (the default), then the setting is queried and the value\n            is returned.\n\n        >>>\n        >>> help(dev.frobbed)\n        Help on method frobbed in module pytek.util:\n\n        frobbed(device, val=None) method of temp.MyDevice instance\n            Configures or queries the value of the ``FROBBED`` setting on the device.\n            If a value is given, then the setting is configured to the given value.\n            If the value is `None` (the default), then the setting is queried and the value\n            is returned.\n\n\n            Querying returns True for "ON", and False for "OFF".\n\n\n            Valid values for configuring are True and False, or synonomously\n            "ON" and "OFF".\n\n        >>>\n        >>>\n\n\n    '
    DEFAULT_DOCTSTR = '\nConfigures or queries the value of the ``%(NAME)s`` setting on the device.\nIf a value is given, then the setting is configured to the given value.\nIf the value is `None` (the default), then the setting is queried and the value\nis returned.\n'

    def __init__(self, name, get=None, set=None, doc=None):
        """
        :param name: Specifies the name of the setting accessed by this object.
            Should be either a `callable` object with a ``__name__`` attribute,
            or a string. Strings will be used directly, callables will be filtered
            through `func_to_name`.
        :param callable get: Optional: if given, passed to `getter`.
        :param callable set: Optional: if given, passed to `setter`.
        :param callable doc: Optional: if given, used as the value of the `doc` attribute.

        """
        if callable(name):
            self.name = self.func_to_name(name)
        else:
            self.name = str(name)
        self.doc = doc
        if doc is None:
            self.doc = self.DEFAULT_DOCTSTR % {'NAME': self.name}
        else:
            self.get = None
            if get is None:
                self.get = lambda device, val: val
            else:
                self.getter(get)
            self.set = None
            if set is None:
                self.set = lambda device, val: str(val)
            else:
                self.setter(set)

    @classmethod
    def configure(cls, device, name, val):
        """
        The final method in this object used to configure the setting, given
        the raw value to be sent to the device. This is called by the `__call__`
        method when appropriate.

        This delegates to the ``send_command`` method of the given `device`.

        :param device: The object on which the ``send_command`` will be invoked.
        :param str name: The name of the setting, usually the value of the `name` attribute.
            This is the first arguments passed to ``send_command``.
        :param str val: The raw value to configure the setting to. This is the
            second argument passed to ``send_command``.
        """
        device.send_command(name, val)

    @classmethod
    def query(cls, device, name):
        """
        The final method in this object used to query the setting, returning
        the raw value from the device. This is called by the `__call__`
        method when appropriate.

        This delegates to the ``send_query`` method of the given `device`.

        :param device: The object on which the ``send_query`` will be invoked.
        :param str name: The name of the setting, usually the value of the `name` attribute.
            This is the only arguments passed to ``send_query``.
        """
        return device.send_query(name)

    def __call__(self, device, val=None):
        """
        __call__(self, device [, val])

        The universal callback which filters values and delegates to `configure` or
        `query` as appropriate.

        If `val` is given (and not `None`), then the setting is configured. The given
        value is first filtered through the callable in the `set` attribute, and
        then passed to `configure`.

        If `val` is not given (or is `None`, the default), then the setting is queried.
        The setting's value is retrieved with `query`, then filtered through the
        callable in this object's `get` attribute before being returned.

        """
        if val is None:
            return self.get(device, self.query(device, self.name))
        self.configure(device, self.name, self.set(device, val))

    def create_method(self, name):
        """
        Creates a method with the given name which can be installed in a class to delegate
        to this object's `__call__` method. Sets the name of the method to `name`,
        and sets the docstr (``__doc__``) to the value of this object's `doc` attribute.

        This is used by `ConfigurableMeta` to replace Configurator instances in the classes
        dictionary with functions.
        """
        config = self

        def c(self, val=None):
            return config(self, val)

        c.__name__ = name
        c.__doc__ = self.doc
        return c

    _Configurator__DOC_APPEND = re.compile('^\\s*\\n(\\s*)\\+\\+\\+\\s*\\n', re.M)
    _Configurator__DOC_PREPEND = re.compile('^\\s*\\n(\\s*)\\-\\-\\-\\s*\\n', re.M)

    def update_doc(self, func):
        """
        If the given function has a docstrig (`__doc__`), then this object's
        `doc` attribute is updated with it. Otherwise, it does nothing.

        If `func`'s docstr begins with ``'+++'`` alone on a line (any amount of leading and trailing whitespace),
        then the remainder of the docstring is *appended* to the existing docstring, instead
        of replacing it.
        """
        if func.__doc__ is not None:
            match = self._Configurator__DOC_APPEND.match(func.__doc__)
            if match:
                indent = re.compile('^' + re.escape(match.group(1)))
                doc = self._Configurator__DOC_APPEND.sub('', func.__doc__)
                doc = os.linesep.join(indent.sub('', line) for line in doc.splitlines())
                self.doc += '\n\n' + doc
            else:
                match = self._Configurator__DOC_PREPEND.match(func.__doc__)
                if match:
                    indent = re.compile('^' + re.escape(match.group(1)))
                    doc = self._Configurator__DOC_PREPEND.sub('', func.__doc__)
                    doc = os.linesep.join(indent.sub('', line) for line in doc.splitlines())
                    self.doc = doc + '\n\n' + self.doc
                else:
                    self.doc = func.__doc__

    @classmethod
    def func_to_name(cls, func):
        """
        Derives a setting name from a function. The implementation here just
        uses the `__name__` attribute of the given `func`, and then uses
        `str.upper()` to make it all upper case.

        This is used in `__init__` if the name is a `callable` object.
        """
        return func.__name__.upper()

    @classmethod
    def boolean(cls, arg, **kwargs):
        """
        A function decorator utility used to create a `Configurator` object
        which handles boolean settings. This ends up delegating to `set_boolean`
        to actually set up the `get` and `set` filters based on responses from
        the decorated function. All keyword arguments passed to this function
        are forwarded to `set_boolean`.

        Similar to `config`, you can invoke this with *implicit arguments*
        or *explicit arguments*

        For **implicit arguments**, you use this method as a function decorator directly,
        and the `name` to use is derived from the decorated function with `func_to_name`.
        In this mode, you can't specify any additional arguments to pass to `set_boolean`.

        For **explicit arguments**, you invoke this method directly, and it returns
        a function decorator. This allows you to pass in a string as the first argument
        to specify the `name` to use, as well as additional keyword arguments to
        be forwarded on to `set_boolean`.

        .. seealso:
            * set_boolean
            * config

        """
        c = cls(arg)
        if callable(arg):
            (c.set_boolean)(arg, **kwargs)
            return c
        else:

            def wrapper(func):
                (c.set_boolean)(func, **kwargs)
                return c

            return wrapper

    @classmethod
    def config(cls, arg):
        """

        A function decorator utility used to create a `Configurator` object and a
        function decorator to configure its `getter`.

        There are two way to invoke this, using *implicit naming* or
        *explicit naming*.

        For **implicit naming***, simply pass a function in directly, or use
        this function directly as a decorator. For instance:

        .. code:: python

            @Configurator.config
            def foobar(self, val):
                return val

        The above code will create a new instance of `cls` (i.e., a Configurator
        object), and will pass the given function ``foobar`` in as the ``name``
        parameter to the constructor. This in turn will use `func_to_name` to
        derive a value for the instance's `name` attribute from the function, by
        default (i.e., in the base `Configurator` class), this is just the name
        of the function in all uppercase.

        The function will also be passed to the instance's `getter` method so
        that the ``foobar`` function becomes the instance's `get` filter.

        This method will then return the Configurator object itself, *not* the
        wrapped function.

        The alternative is **explicit naming**, in which this function is not
        used *as* a function wrapper, but invoked to *return* a function wrapper.
        This gives you some added flexibility such as explitictly giving the `name`
        to use for the Configurator object. Otherwise, the behavior is essentially
        the same.

        For instance:

        .. code:: python

            @Configurator.config('BAZ:RUFFLE')
            def foobar(self, val):
                return val

        In this case, even though the wrapped function has the same name, ``"foobar"``,
        the created Configurator object will have a ``name`` of ``"BAZ:RUFFLE"``.
        Other than that, the effects are the same.

        In either case, when code like this appears in a class definition,
        it means that class will have an attribute named ``foobar`` whose value
        is a Configurator object. If this class is using the `~Configurator.ConfigurableMeta`
        metaclass, then this attribute will be replaced by a proper method
        generated by the Configurator's `create_method` method.

        Also note that when the wrapped function is passed to the Configurator's
        `getter` method, this method will also pass it to `update_doc`, so if the
        wrapped function has a docstring, the Configurator object's `doc` attribute
        will be set accordingly. When the `~Configurator.ConfigurableMeta` gets
        a hold of it, the corresponding method it adds to the class will receive
        this docstr from the Configurator object.

        Note that for the remainder of the class definition, you can
        use the generated Configurator object. For instance, you can follow up
        either of the above examples with the following:

        .. code :: python

            @foobar.setter
            def foobar(self, val):
                if val is False:
                    return "OFF"
                return "ON"

        Since at this point the ``foobar`` symbol is actually a Configurator
        object, you can use its other decorators such as `setter` and `getter`.

        """
        c = cls(arg)
        if callable(arg):
            c.getter(arg)
            return c
        else:

            def wrapper(func):
                c.getter(func)
                return c

            return wrapper

    def setter(self, func):
        """
        A function wrapper which sets this object's `set` attribute to the given
        function and passes the function to `update_doc`, then returns `self`.

        The given function should take two arguments and return a string. The
        first argument will be the device on which the `send_command` method
        is invoked, the second argument will be the client supplied value they
        want to configure the setting to. The function should return a corresponding
        string which will actually be sent to the device.
        """
        self.set = func
        self.update_doc(func)
        return self

    def getter(self, func):
        """
        Like `setter`, but sets the object's `get` attribute, used for querying the
        setting from the device.

        This is a function wrapper which sets this object's `get` attribute to the given
        function and passes the function to `update_doc`, then returns `self`.

        The given function should take two arguments and return a string. The
        first argument will be the device on which the `send_query` method
        is invoked, the second argument will be the value returned from the device
        by `send_query`. The function should return a corresponding
        value which will be returned to the user to reflect the string returned
        by the device.
        """
        self.get = func
        self.update_doc(func)
        return self

    def set_boolean(self, func, strict=False, default=False, nocase=False):
        """
        Configures the objects `set` and `get` filters based on a boolean setting.

        A boolean setting means the setting has a set of possible values that are
        partitioned into two subsets: true values and false values. On the python side,
        any value in these subsets corresponds to a value of `True` or `False`, respectively.

        This method sets up the object to filter values accordingly, so that querying
        the setting always returns `True` or `False`, and configuring the setting can be
        done with `True` or `False`.

        To do so, you have to pass in a function which can be evaluated immediately to get the
        set of true values and the set of false values. The function should take a single
        boolean argument, if the argument value is `True`, return the set of true values,
        otherwise, return the set of false values. The method will then create appropriate
        set and get filters based on these values and the other parameters passed into
        this function (see below).

        The sets of true values and false values returned by `func` must be sequences.
        The first value in each sequence will be used as the *canonical* value, meaning the
        ones that will actually be passed to the device for the corresponding value. All other
        values in the sets will be acceptable responses from the device for queries, and
        will result in the corresponding boolean value being returned to the caller.

        .. seealso::
            `boolean`

        :param callable func:   This function will be called twice, immediately. Once with a value
            of `True`, which should return a sequence of true values; and once with a value of
            `False`, which should return a sequence of false values.

        :param bool strict:     Optional, default is `False`. If `True`, then the generated
            `set` and `get` filters will be strict about values. The `set` filter will only
            accept boolean values, and will raise a `TypeError` otherwise. The `get` filter
            will only accept values from the true- and false- value sets, and will raise
            a `ValueError` if the device returns anything else.

            If the value of the parameter is `False`, the generated functions are not as
            strict, and will not raise exceptions for unrecognized values (the way it handles
            unrecognized values depends on the value of the `default` parameter).
            For the non-strict `set` filter, values are simply evaluated as bools to choose
            which value to send.

        :param bool default:    Optional, default value is `False`. This is only used if
            `strict` is `False`, in which case it determines the *default* value when an
            unrecognized value is encountered.

        :param bool nocase:     Optional, default value is `False`. If `True`, then values are
            considered case-insensitive.

        """
        t_vals = func(True)
        f_vals = func(False)
        pretty_val = lambda val: '``"%s"``' % val
        val_list = lambda vals: ', '.join(pretty_val(v) for v in vals)
        d = dict(T_VALS=(val_list(t_vals)),
          F_VALS=(val_list(f_vals)),
          TRUE=(pretty_val(t_vals[0])),
          FALSE=(pretty_val(f_vals[0])))
        convert = lambda val: val
        if nocase:
            convert = lambda val: val.lower()
            t_vals = map(convert, t_vals)
            f_vals = map(convert, f_vals)
        else:
            if strict:

                def g(device, val):
                    val = convert(val)
                    if val in t_vals:
                        return True
                    if val in f_vals:
                        return False
                    raise ValueError('Unexpected value returned from device: %r' % val)

                def s(device, val):
                    if val is True:
                        return t_vals[0]
                    if val is False:
                        return f_vals[0]
                    raise TypeError('Expected boolean value, received: %r' % val)

            else:
                if default:

                    def g(device, val):
                        return convert(val) not in f_vals

                    def s(device, val):
                        if bool(val):
                            return f_vals[0]
                        else:
                            return t_vals[0]

                else:

                    def g(device, val):
                        return convert(val) in t_vals

                    def s(device, val):
                        if bool(val):
                            return t_vals[0]
                        else:
                            return f_vals[0]

        g.__doc__ = g.__doc__ % d
        s.__doc__ = s.__doc__ % d
        self.getter(g)
        self.setter(s)
        self.update_doc(func)

    class ConfigurableMeta(type):
        __doc__ = "\n        This is a meta class that can be added to classes to more easily support\n        the use of `Configurator` objects as pseudo-methods.\n\n        The meta class extends the `__new__` function to find all instances of\n        `Configurator` in the class's dictionary, and replace it with a method\n        created by the Configurator's `~Configurator.create_method` method.\n\n        See the example code in the documentation for `Configurator` for an\n        example.\n        "

        def __new__(meta, name, bases, dct):
            for attr, val in dct.items():
                if isinstance(val, Configurator):
                    method = val.create_method(attr)
                    method.__doc__ = '%s([val])\n\n' % attr + method.__doc__
                    dct[attr] = method

            return super(Configurator.ConfigurableMeta, meta).__new__(meta, name, bases, dct)


class Configurable(object):
    __doc__ = '\n    Just a simple base classes that uses `~Configurator.ConfigurableMeta`\n    as the metaclass.\n    '
    __metaclass__ = Configurator.ConfigurableMeta