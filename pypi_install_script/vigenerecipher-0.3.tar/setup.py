# coding=utf-8
from setuptools import setup, find_packages

setup(name='vigenerecipher',
      version='0.3',
      description='The Vigenère cipher is a cryptography method that uses a series of different Caesar numbers based '
                  'on the letters of a password. This is a simplified version of a more general polyalphabetical '
                  'substitution figure invented by Leon Battista Alberti about 1465.',
      url='https://github.com/andersongomes001/vigenerecipher',
      author='Anderson Gomes',
      author_email='comprasgomes@hotmail.com',
      license='GNU GPL v3',
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False)