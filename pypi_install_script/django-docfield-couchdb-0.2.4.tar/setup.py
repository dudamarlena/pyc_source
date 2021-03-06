#/usr/bin/env python

name = 'docfield'
long_name = 'django-docfield-couchdb'
version = '0.2.4'
packages = [name]
description = "Django fields for representing CouchDB docs and more."

keywords = [
    'django','couchdb','json','NoSQL','database',
    'utility','fields','models','trees','fields',
]

long_description = """
    
    Django fields and other add-ons that represent key CouchDB data structures:
    
    *) Docs, which can authoratively reside in either Couch or your Django RDBMS
    *) Arbitrary JSON subtrees
    *) CouchDB _id and _rev identifiers
    *) NEW in 1.1: an error-free setup.py install experience!
    
    And MORE!!! Coming soon of course.
    
"""


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Environment :: Other Environment',
    'Environment :: Plugins',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Topic :: Database',
    'Topic :: Utilities',
]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(

    name=long_name, version=version, description=description,
    long_description=long_description,
    download_url=('http://github.com/fish2000/%s/zipball/master' % long_name),

    author=u"Alexander Bohn",
    author_email='fish2000@gmail.com',
    url='http://github.com/fish2000/%s' % long_name,
    license='GPLv2',
    keywords=', '.join(keywords),
    platforms=['any'],
    
    include_package_data=True,
    
    packages=[]+packages,
    package_dir={},
    package_data={},
    install_requires=['django-delegate', 'couchdbkit'],

    classifiers=classifiers+[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy'],
)

