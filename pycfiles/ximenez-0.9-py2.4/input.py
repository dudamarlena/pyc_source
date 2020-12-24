# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/input.py
# Compiled at: 2008-01-19 12:05:43
"""Define ``InputAware`` mixin.

$Id: input.py 45 2008-01-19 17:05:45Z damien.baty $
"""
try:
    import readline
except ImportError:
    pass

import logging
from getpass import getpass
from types import StringType

def xim_raw_input(prompt=None):
    return raw_input(prompt)


def xim_getpass(prompt=None):
    return getpass(prompt)


class InputAware:
    """Mixin class which defines input-related methods."""
    __module__ = __name__
    _input = {}
    _input_info = ()
    _multiple_input = False

    def getInput(self, cl_input=None):
        """Get input from the user or from the command line argument
        if ``cl_input`` is not empty.

        The default handling of ``cl_input`` supposes that it is
        composed by a ';;'-separated list of ``key=value``
        pairs. E.g.::

            path=file.txt;;userid=bob

        will result in the following ``_input`` mapping::

            {'path': 'file.txt',
             'userid': 'bob'}

        Errors are not catched and will therefore raise exceptions.
        """
        if cl_input:
            for pair in cl_input.split(';;'):
                (key, value) = pair.split('=')
                self._input[key] = value

        elif self._multiple_input:
            self._input = self.askForMultipleInput()
        else:
            self._input = self.askForInput()

    def getInputInfo(self):
        """Return a tuple of mappings which describes information
        needed by the collector.

        The mappings looks like::

            {'name': <string>,
             'prompt': <string>,
             'required': <boolean>,
             'default': <string>,
             'hidden': <boolean>,
             'validators': <sequence of strings or callables>,
            }

        where:

        - ``name`` is the name of the argument;

        - ``prompt`` is the string which will be displayed to the
          user;

        - ``required`` is an optional boolean which tells whether or
          not the user input is required. Default is ``False``;

        - ``default`` is a default value given to the argument if no
          value is given (though only if it is not reduired);

        - ``hidden`` is an optional boolean which tells whether the
          user input has to be hidden (e.g. for a password). Default
          is ``False``;

        - ``validators`` is an optional sequence of validators. Each
          validator may be either a string (which should be a method
          of the object calling ``getInput()``) or a callable (a
          function, a lambda expression, etc.)

        FIXME: we could also have a 'vocabulary' key which would:
        - enforce the value to be in a restricted set of values
        - provide completion feature
        """
        return self._input_info

    def askForInput(self, input_info=None):
        """Ask user for input, based on the needed informations which
        are in ``input_info`` or returned by ``getInputInfo()`` if the
        former is ``None``.

        **WARNING:** this method does **not** store the user input in
        the object. It only returns it.
        """

        def _validate(validators, value):
            """Run ``validators`` on ``value``."""
            for validator in validators:
                error = False
                if type(validator) == StringType:
                    validate = getattr(self, validator, None)
                    if validate is None:
                        error = True
                    elif not validate(value):
                        return False
                elif callable(validator):
                    if not validator(value):
                        return False
                if error:
                    logging.error('Could not infer what to do with this validator: %s', validator)

            return True

        if input_info is None:
            input_info = self.getInputInfo()
        user_input = {}
        for info in input_info:
            while 1:
                ask = xim_raw_input
                if info.get('hidden'):
                    ask = xim_getpass
                value = ask(info['prompt'])
                if not value and not info.get('required') and info.get('default'):
                    value = info['default']
                if value or not info.get('required'):
                    if _validate(info.get('validators', ()), value):
                        user_input[info['name']] = value
                        break

        return user_input

    def askForMultipleInput(self):
        """Ask user for more than one input, until (s)he presses
         ``^C``.
        """
        user_input = []
        while True:
            try:
                user_input.append(self.askForInput())
            except KeyboardInterrupt:
                break

        return user_input