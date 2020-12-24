"""
setup.py

Setup configuration for the package.

:author:        Stephen Stauts
:created:       07/03/2020   (DD/MM/YYYY)
:copyright:     © 2020 Stephen Stauts. All Rights Reserved.
"""

# Standard Packages
import setuptools
from pathlib import Path


PACKAGE_NAME = 'futils'     # The name used when importing projects
PIP_NAME = 'futils'         # Package name used by PyPI and pip
P_ROOT = Path(__file__).absolute().parents[0]


def get_version():
    """
    Access package version without importing.

    :reference: https://github.com/paramiko/paramiko/blob/master/setup.py#L38
    """
    _locals = {}
    with open(Path(P_ROOT, 'src', PACKAGE_NAME, 'version.py')) as f:
        exec(f.read(), None, _locals)
    return _locals['__version__']


def get_long_description():
    """Read the contents of the README file."""
    p_readme = Path(P_ROOT, 'README.md')
    with open(str(p_readme.absolute()), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


setuptools.setup(
    name=PIP_NAME,
    version=get_version(),
    description='A collection of fancy utilities for Python.',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/kyberdin/futils',
    author='Stephen Stauts',
    author_email='kyberdin.git@gmail.com',
    license='MIT',
    keywords='utilities util',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.5',
    package_dir = {'': 'src'},
    packages=[
        PACKAGE_NAME
    ],
    install_requires=[
    ],
)
