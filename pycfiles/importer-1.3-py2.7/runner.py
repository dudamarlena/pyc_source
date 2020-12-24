# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/importer_tests/runner.py
# Compiled at: 2014-02-03 17:56:37
"""

    importer: testrunner
    ~~~~~~~~~~~~~~~~~~~~

    this file collects and runs ``importer``'s testsuite.

    :author: Sam Gammon <sam@keen.io>
    :license: This software follows the MIT (OSI-approved)
              license for open source software. A truncated
              version is included here; for full licensing
              details, see ``LICENSE.md`` in the root directory
              of the project.

              Copyright (c) 2013, Keen IO

              The above copyright notice and this permission notice shall be included in
              all copies or substantial portions of the Software.

              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
              THE SOFTWARE.

"""
import os, sys, unittest
_TEST_PATHS = [
 'test_tz',
 'test_mix',
 'test_keen',
 'test_mixpanel']

def fix_path():
    """ Add ``.`` and ``dir/lib`` to ``sys.path``. """
    for path in (os.path.dirname(__file__),
     os.path.dirname(os.path.dirname(__file__)),
     os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lib')):
        sys.path.insert(0, path)


def load_module(path):
    """ __main__ testing entrypoint for `apptools.model`. """
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromName(path))
    return suite


def load(paths=None):
    """ __main__ entrypoint """
    mixtests = unittest.TestSuite()
    if paths is None:
        paths = _TEST_PATHS[:]
    for path in paths:
        mixtests.addTest(load_module(path))

    return mixtests


def run(suite=None):
    """ Optionally allow switching between XML or text output, if supported. """
    fix_path()
    if suite is None:
        suite = load()
    if hasattr(unittest, 'TestRunner'):
        runner = unittest.TestRunner
    else:
        runner = unittest.TextTestRunner
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if len(args) == 2:
            format, output = tuple(args)
            if format.lower().strip() == 'xml':
                try:
                    import xmlrunner
                except ImportError:
                    print 'ERROR! XML testrunner (py module `xmlrunner`) could not be imported. Please run in text-only mode.'
                    exit(1)

                xmlrunner.XMLTestRunner(output=output).run(suite)
            elif format.lower().strip() == 'text':
                return runner(verbosity=5, output=output).run(suite)
        else:
            return runner(verbosity=5, output=output).run(suite)
    return runner(verbosity=5).run(suite)