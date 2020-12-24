from distutils.core import setup
from setuptools import find_packages

setup(
    name='pydevtools',
    version='0.4',
        author="AndersBallegaard",
    author_email="anderstb@hotmail.dk",
    packages=find_packages(exclude="tests/"),
    license='MIT',
    long_description=open('README.txt').read(),
)