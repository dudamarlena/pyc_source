from setuptools import setup
from setuptools import find_packages

version = '0.1.2'

setup(name='utilsfunc',
      version=version,
      description='Some handy functions help you to easy working',
      install_requires=['numba', 'nltk'],
      include_package_data=True,
      packages=find_packages())
