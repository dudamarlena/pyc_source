# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

root_dir = path.abspath(path.dirname(__file__))

with open(path.join(root_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tirsvadcms_packagemanager',
    version='0.1.0b',
    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[

        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',

    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    install_requires=[
        'distro',
    ],
)