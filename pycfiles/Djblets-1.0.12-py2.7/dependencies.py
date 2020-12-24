# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/dependencies.py
# Compiled at: 2019-06-12 01:17:17
"""Version information for certain Djblets dependencies.

This contains constants that other parts of Djblets and consumers of Djblets
can use to look up information on major dependencies of Djblets.

The contents in this file might change substantially between releases. If
you're going to make use of data from this file, code defensively.
"""
from __future__ import unicode_literals
django_doc_major_version = b'1.6'
django_version = b'>=1.6.11,<1.10.999'
lesscss_npm_dependencies = {b'less': b'3.9.0', 
   b'less-plugin-autoprefix': b'2.0.0'}
uglifyjs_npm_dependencies = {b'uglify-js': b'2.4.10'}
babel_npm_dependencies = {b'babel-cli': b'6.5.1', 
   b'babel-preset-es2015': b'6.5.0', 
   b'babel-plugin-dedent': b'2.0.0'}
npm_dependencies = {}
npm_dependencies.update(lesscss_npm_dependencies)
npm_dependencies.update(uglifyjs_npm_dependencies)
npm_dependencies.update(babel_npm_dependencies)
package_dependencies = {b'Django': django_version, 
   b'django-pipeline': b'>=1.6.14,<1.6.999', 
   b'dnspython': b'>=1.14.0', 
   b'feedparser': b'>=5.1.2', 
   b'pillowfight': b'', 
   b'publicsuffix': b'>=1.1', 
   b'python-dateutil': b'>=1.5', 
   b'pytz': b''}

def build_dependency_list(deps, version_prefix=b''):
    """Build a list of dependency specifiers from a dependency map.

    This can be used along with :py:data:`package_dependencies`,
    :py:data:`npm_dependencies`, or other dependency dictionaries to build a
    list of dependency specifiers for use on the command line or in
    :file:`setup.py`.

    Args:
        deps (dict):
            A dictionary of dependencies.

    Returns:
        list of unicode:
        A list of dependency specifiers.
    """
    return [ b'%s%s%s' % (dep_name, version_prefix, dep_version) for dep_name, dep_version in deps.items()
           ]