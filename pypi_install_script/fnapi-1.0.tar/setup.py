import setuptools
from setuptools import setup, find_packages
 
setup(name='fnapi',
      version='1.0',
      url='https://github.com/1xev3/FnApi',
      license='MIT',
      author='Dima Suzmin',
      author_email='diman.suzmin@yandex.ru',
      description='Simple library for fortnite things',
      packages=setuptools.find_packages(),
      long_description=open('README.md').read(),
      classifiers=['Programming Language :: Python'],
      zip_safe=False)