#!/usr/bin/env python

import setuptools
from distutils.core import setup, Extension

setup(
    name = 'pdbparse',
    version = '1.5',
    description = 'Python parser for Microsoft PDB files',
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'Brendan Dolan-Gavitt',
    author_email = 'brendandg@gatech.edu',
    url = 'https://github.com/moyix/pdbparse/',
    packages = ['pdbparse'],
    install_requires = ['construct>=2.9', 'construct<2.10', 'pefile'],
    classifiers = [
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
    ],
    ext_modules = [Extension('pdbparse._undname', sources = ['src/undname.c', 'src/undname_py.c'])],
    include_package_data=True,
    scripts = [
        'examples/pdb_dump.py',
        'examples/pdb_get_syscall_table.py',
        'examples/pdb_lookup.py',
        'examples/pdb_print_ctypes.py',
        'examples/pdb_print_gvars.py',
        'examples/pdb_print_tpi.py',
        'examples/pdb_tpi_vtypes.py',
        'examples/symchk.py',
    ])
