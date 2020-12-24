# coding: UTF-8
from distutils.core import setup
from os import path


setup(
    name             = 'ObjectProxy',
    version          = '0.2',
    license          = 'BSD',
    platforms        = 'any',
    url              = 'https://github.com/Montegasppa/ObjectProxy',
    download_url     = 'https://github.com/Montegasppa/ObjectProxy/archive/devel.zip',
    py_modules       = ['object_proxy', 'object_proxy._lambda_relations'],
    author           = 'Rodrigo Cacilhας',
    author_email     = 'batalema@cacilhas.info',
    description      = 'proxy to objects with lazy import',
    install_requires = [],
    classifiers      = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
