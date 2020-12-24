# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/utils/Settings.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 7365 bytes
__doc__ = 'The ``cdt.utils.Settings`` module defines the settings used in the toolbox,\nsuch as the default hardware parameters; and the tools to autodetect the\nhardware. All parameters are overridable by accessing the ``cdt.SETTINGS``\nobject, a unique instance of the ``cdt.utils.ConfigSettings`` class.\n\nThe various attributes of the ``cdt.SETTINGS`` configuration object are:\n\n1. ``cdt.SETTINGS.NJOBS``\n2. ``cdt.SETTINGS.GPU``\n3. ``cdt.SETTINGS.default_device``\n4. ``cdt.SETTINGS.autoset_config``\n5. ``cdt.SETTINGS.verbose``\n6. ``cdt.SETTINGS.rpath``\n\nThe hardware detection revolves around the presence of GPUs. If GPUs are\npresent, ``cdt.SETTINGS.GPU`` is set to ``True`` and the number of jobs\nis set to the number of GPUs. Else the number of jobs is set to the number\nof CPUs. Another test performed at startup is to check if an R framework\nis available, unlocking additional features of the toolbox.\n\n``cdt.SETTINGS.rpath`` allows the user to set a custom path for the Rscript\nexecutable. It should be overriden with the full path as a string.\n\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import ast, os, warnings, multiprocessing, GPUtil

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class ConfigSettings(object):
    """ConfigSettings"""
    __slots__ = ('NJOBS', 'GPU', 'default_device', 'autoset_config', 'verbose', 'rpath')

    def __init__(self):
        super(ConfigSettings, self).__init__()
        self.NJOBS = 8
        self.GPU = 0
        self.autoset_config = True
        self.verbose = True
        self.default_device = 'cpu'
        self.rpath = 'Rscript'
        if self.autoset_config:
            self = autoset_settings(self)
        self.default_device = 'cuda:0' if self.GPU else 'cpu'

    def __setattr__(self, attr, value):
        if attr == 'GPU':
            if value:
                if not self.GPU:
                    if self.default_device == 'cpu':
                        self.default_device = 'cuda:0'
        super(ConfigSettings, self).__setattr__(attr, value)
        if attr == 'rpath':
            if object.__getattribute__(self, 'rpath') is not None:
                from .R import RPackages
                RPackages.reset()

    def get_default(self, *args, **kwargs):
        r"""Get the default parameters as defined in the Settings instance.

        This function proceeds to seamlessly retrieve the argument to pass
        through, depending on either it was overidden or not: If no argument
        was overridden in a function of the toolbox, the default argument will
        be set to ``None``, and this function will retrieve the default
        parameters as defined by the ``cdt.SETTINGS`` 's attributes.

        It has two modes of processing:

        1. \**kwargs for retrieving a single argument: ``get_default(argument_name=value)``.
        2. \*args through a list of tuples of the shape ``('argument_name', value)`` to retrieve multiple values at once.
        """

        def retrieve_param(i):
            try:
                return self.__getattribute__(i)
            except AttributeError:
                if i == 'device':
                    return self.default_device
                else:
                    return self.__getattribute__(i.upper())

        if len(args) == 0:
            if len(kwargs) == 1:
                if kwargs[list(kwargs.keys())[0]] is not None:
                    return kwargs[list(kwargs.keys())[0]]
            if len(kwargs) == 1:
                return retrieve_param(list(kwargs.keys())[0])
            raise TypeError('As dict is unordered, it is impossible to givethe parameters in the correct order.')
        else:
            out = []
            for i in args:
                if i[1] is None:
                    out.append(retrieve_param(i[0]))
                else:
                    out.append(i[1])

            return out


def autoset_settings(set_var):
    """Autoset GPU parameters using CUDA_VISIBLE_DEVICES variables.

    Return default config if variable not set.
    :param set_var: Variable to set. Must be of type ConfigSettings
    """
    try:
        devices = ast.literal_eval(os.environ['CUDA_VISIBLE_DEVICES'])
        if type(devices) != list:
            if type(devices) != tuple:
                devices = [
                 devices]
        if len(devices) != 0:
            set_var.GPU = len(devices)
            set_var.NJOBS = len(devices)
            warnings.warn('Detecting CUDA device(s) : {}'.format(devices))
    except KeyError:
        try:
            set_var.GPU = len(GPUtil.getAvailable(order='first', limit=8, maxLoad=0.5,
              maxMemory=0.5,
              includeNan=False))
            if not set_var.GPU:
                warnings.warn('No GPU automatically detected. Setting SETTINGS.GPU to 0, and SETTINGS.NJOBS to cpu_count.')
                set_var.GPU = 0
                set_var.NJOBS = multiprocessing.cpu_count()
            else:
                set_var.NJOBS = set_var.GPU
                warnings.warn('Detecting {} CUDA device(s).'.format(set_var.GPU))
        except ValueError:
            warnings.warn('No GPU automatically detected. Setting SETTINGS.GPU to 0, and SETTINGS.NJOBS to cpu_count.')
            set_var.GPU = 0
            set_var.NJOBS = multiprocessing.cpu_count()

    return set_var


SETTINGS = ConfigSettings()