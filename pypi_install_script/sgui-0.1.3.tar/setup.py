from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='sgui',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version='0.1.3',
      description='A simple GUI library for Python',
      url='https://github.com/DGriffin91/sgui',
      author='DGriffin91',
      author_email='sgui@dgdigital.net',
      license='MIT',
      packages=['sgui'],
      zip_safe=False)