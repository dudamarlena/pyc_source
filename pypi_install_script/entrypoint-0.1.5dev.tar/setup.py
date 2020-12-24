from setuptools import setup, find_packages
import sys, os

version = '0.1.5'

setup(name='entrypoint',
      version=version,
      description="A decorator to interact with argparse based on function signature.",
      long_description=open('README.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='argparse decorator optparse signature command-line',
      author='Conrad Irwin',
      author_email='conrad.irwin@gmail.com',
      url='',
      license='Python license',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'argparse', 'decorator',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
