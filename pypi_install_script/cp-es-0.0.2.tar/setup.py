from setuptools import setup, find_packages
import sys, os

version = '0.0.2'

setup(name='cp-es',
      version=version,
      description="this is Carpool Project psubpackage: cp-es",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='petergra',
      author_email='lvpet@esquel.com',
      url='https://www.m.general.gitsite.net',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'elasticsearch'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
