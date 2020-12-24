# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/utils/R.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 8044 bytes
__doc__ = 'Loading and executing functions from R packages.\n\nThis module defines the interface between R and Python using subprocess.\nAt the initialization, the toolbox checks if R is available and sets\n``cdt.SETTINGS.r_is_available`` to ``True`` if the R framework is detected.\nElse, this module is deactivated.\n\nNext, each time an R function is called, the availability of the R package is\ntested using the ``DefaultRPackages.check_R_package`` function. The number of\navailable packages is limited and the list is defined in ``DefaultRPackages``.\n\nIf the package is available, the ``launch_R_script`` proceeds to the execution\nof the function, by:\n\n1. Copying the R script template and modifying it with the given arguments\n2. Copying all the data to a temporary folder\n3. Launching a R subprocess using the modified template and the data, and\n   the script saves the results in the temporary folder\n4. Retrieving all the results in the Python process and cleaning up all the\n   temporary files.\n\n.. note::\n   For custom R configurations/path, a placeholder for the Rscript executable\n   path is available at ``cdt.SETTINGS.rpath``. It should be overriden with\n   the full path as a string.\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import os, warnings, fileinput, subprocess, uuid
from shutil import copy, rmtree
from tempfile import gettempdir
import cdt.utils.Settings

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning
init = True

class DefaultRPackages(object):
    """DefaultRPackages"""
    __slots__ = ('init', 'pcalg', 'kpcalg', 'bnlearn', 'sparsebn', 'D2C', 'SID', 'CAM',
                 'RCIT')

    def __init__(self):
        """Init the values of the packages."""
        self.reset()

    def __repr__(self):
        """Representation."""
        return str(['{}: {}'.format(i, getattr(self, i)) for i in self.__slots__])

    def __str__(self):
        """For print purposes."""
        return str(['{}: {}'.format(i, getattr(self, i)) for i in self.__slots__])

    def reset(self):
        self.init = True
        self.pcalg = None
        self.kpcalg = None
        self.bnlearn = None
        self.sparsebn = None
        self.D2C = None
        self.SID = None
        self.CAM = None
        self.RCIT = None
        self.init = False

    def __getattribute__(self, name):
        """Test if libraries are available on the fly."""
        out = object.__getattribute__(self, name)
        if out is None and not object.__getattribute__(self, 'init'):
            availability = self.check_R_package(name)
            setattr(self, name, availability)
            return availability
        else:
            return out

    def check_R_package(self, package):
        """Execute a subprocess to check the package's availability.

        Args:
            package (str): Name of the package to be tested.

        Returns:
            bool: `True` if the package is available, `False` otherwise
        """
        test_package = not bool(launch_R_script(('{}/R_templates/test_import.R'.format(os.path.dirname(os.path.realpath(__file__)))), {'{package}': package}, verbose=True))
        return test_package


def launch_R_script(template, arguments, output_function=None, verbose=True, debug=False):
    """Launch an R script, starting from a template and replacing text in file
    before execution.

    Args:
        template (str): path to the template of the R script
        arguments (dict): Arguments that modify the template's placeholders
            with arguments
        output_function (function): Function to execute **after** the execution
            of the R script, and its output is returned by this function. Used
            traditionally as a function to retrieve the results of the
            execution.
        verbose (bool): Sets the verbosity of the R subprocess.
        debug (bool): If True, the generated scripts are not deleted.

    Return:
        Returns the output of the ``output_function`` if not `None`
        else `True` or `False` depending on whether the execution was
        successful.
    """
    base_dir = '{0!s}/cdt_R_script_{1!s}'.format(gettempdir(), uuid.uuid4())
    os.makedirs(base_dir)
    rpath = cdt.utils.Settings.SETTINGS.get_default(rpath=None)
    try:
        scriptpath = '{}/instance_{}'.format(base_dir, os.path.basename(template))
        copy(template, scriptpath)
        with fileinput.FileInput(scriptpath, inplace=True) as (file):
            for line in file:
                mline = line
                for elt in arguments:
                    mline = mline.replace(elt, arguments[elt])

                print(mline, end='')

        if output_function is None:
            output = subprocess.call(('{} --vanilla {}'.format(rpath, scriptpath)), shell=True, stdout=(subprocess.DEVNULL),
              stderr=(subprocess.DEVNULL))
        else:
            if verbose:
                process = subprocess.Popen(('{} --vanilla {}'.format(rpath, scriptpath)), shell=True)
            else:
                process = subprocess.Popen(('{} --vanilla {}'.format(rpath, scriptpath)), shell=True, stdout=(subprocess.DEVNULL),
                  stderr=(subprocess.DEVNULL))
            process.wait()
            output = output_function()
    except Exception as e:
        if not debug:
            rmtree(base_dir)
        raise e
    except KeyboardInterrupt:
        if not debug:
            rmtree(base_dir)
        raise KeyboardInterrupt

    if not debug:
        rmtree(base_dir)
    return output


RPackages = DefaultRPackages()
init = False