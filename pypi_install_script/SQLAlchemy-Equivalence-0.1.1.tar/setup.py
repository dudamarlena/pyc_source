"""
SQLAlchemy-Equivalence
----------------------

Provides natural equivalence support for SQLAlchemy declarative models.
"""

from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='SQLAlchemy-Equivalence',
    version='0.1.1',
    url='https://github.com/kvesteri/sqlalchemy-equivalence',
    license='BSD',
    author='Konsta Vesterinen',
    author_email='konsta@fastmonkeys.com',
    description=(
        'Provides natural equivalence support for SQLAlchemy '
        'declarative models.'
    ),
    long_description=__doc__,
    packages=['sqlalchemy_equivalence'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'SQLAlchemy==0.7.8',
    ],
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
