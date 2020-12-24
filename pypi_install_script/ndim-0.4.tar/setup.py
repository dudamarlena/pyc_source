from distutils.core import setup

with open('README.md') as fd:
    long_description = fd.read()


setup(
    name                = 'ndim',
    packages            = [],
    version             = '0.4',
    py_modules          = ['ndim', 'ndim_base', 'ndim_arc', 'ndim_bezier'],
    description         = 'Utility functions for manipulating points N-dimensional geometry.',
    author              = 'David McEwan',
    author_email        = 'cogitocumimpune@hotmail.com',
    license             = 'GLPv3',
    platforms           = 'Python >2.6 including 3.x (OS Independent)',
    url                 = 'https://github.com/DavidMcEwan/ndim',
    package_data       = {'package': ['*.py', 'README.md']},
    
    classifiers         = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
                          ],
    
    long_description    = long_description
)
