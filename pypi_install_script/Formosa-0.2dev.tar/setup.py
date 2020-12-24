from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name='Formosa',
      version='0.2dev',
      description='Package for processing user input to Web applications',
      author='Nick Murphy',
      author_email='njmurphy@gmail.com',
      packages=find_packages())
