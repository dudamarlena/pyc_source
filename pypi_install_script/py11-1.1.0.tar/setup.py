from setuptools import setup, find_packages

setup(
  name='py11',
  version='1.1.0',
  description='Provide a Python3 interface for Pybind11',
  long_description='Provide a Python3 interface for Pybind11',
  url='http://cct.lsu.edu/~sbrandt/',
  author='Steven R. Brandt',
  author_email='steven@stevenrbrandt.com',
  license='LGPL',
  packages=['py11'],
  install_requires=['pybind11']
)
