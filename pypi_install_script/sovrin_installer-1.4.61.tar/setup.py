from distutils.core import setup

from setuptools import find_packages

setup(
    name='sovrin_installer',
    version='1.4.61',
    description='Sovrin Installer',
    packages=find_packages(exclude=['test', 'test.*', 'docs', 'docs*']),
    license='__license__',
    long_description='Sovrin Installer (cross platform)',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    scripts=['scripts/run-sovrin-installer']
)
