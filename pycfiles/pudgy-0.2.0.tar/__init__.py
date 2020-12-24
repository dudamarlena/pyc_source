# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/__init__.py
# Compiled at: 2006-12-29 16:27:16
__doc__ = "Pudge package.\n\nThe `pudge.generator.Generator` class can be used to generate Python\ndocumentation::\n\n    from pudge.generator import Generator\n    generator = Generator()\n    generator.title = 'Foo Documentation'\n    generator.license = 'gnu'\n    generator.dest_dir = '/tmp/documentation'\n    generator.modules = ['foo']\n    generator()\n    \nThis package contains modules for generating documentation from Python\nsource code. The `pudge.generator.Generator` class uses the `peruser`\nand `scanner` modules to inspect a package/module hierarchy, the\n`colorizer` and `rst` modules to generate HTML files and fragments.\n\n"
import logging
log = logging.getLogger('pudge')
__all__ = [
 'generator', 'scanner', 'colorizer', 'cli', 'rst', 'log', 'browser']
__author__ = 'Ryan Tomayko <rtomayko@gmail.com>'
__date__ = '$Date: 2006-12-29 13:45:52 -0800 (Fri, 29 Dec 2006) $'
__revision__ = '$Revision: 132 $'
__url__ = '$URL: svn://lesscode.org/pudge/trunk/pudge/__init__.py $'
__copyright__ = 'Copyright 2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'
__version__ = '0.1.3'