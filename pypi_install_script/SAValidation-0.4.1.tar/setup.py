from __future__ import absolute_import

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.develop import develop as STDevelopCmd


class DevelopCmd(STDevelopCmd):
    def run(self):
        # add in requirements for testing only when using the develop command
        self.distribution.install_requires.extend([
            'mock',
            'nose',
        ])
        STDevelopCmd.run(self)

cdir = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(cdir, 'readme.rst')).read()
CHANGELOG = open(os.path.join(cdir, 'changelog.rst')).read()
VERSION = open(os.path.join(cdir, 'savalidation', 'version.txt')).read().strip()

setup(
    name='SAValidation',
    version=VERSION,
    description="Active Record like validation on SQLAlchemy declarative model objects",
    long_description=README + '\n\n' + CHANGELOG,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database',
    ],
    author='Randy Syring',
    author_email='randy.syring@level12.io',
    url='https://github.com/blazelibs/sqlalchemy-validation',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    cmdclass={'develop': DevelopCmd},
    install_requires=[
        'SQLAlchemy>=0.7.6',
        'python-dateutil',
        'FormEncode>={}'.format(
            '1.2' if sys.version_info.major == 2 else '1.3.0a1',
        ),
        'six',
    ],
)
