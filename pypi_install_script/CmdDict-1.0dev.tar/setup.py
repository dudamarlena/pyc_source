from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='CmdDict',
      version=version,
      description="A command line dictionary",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='dictionary command-line',
      author='Said Ozcan',
      author_email='said@ozcan.co',
      url='http://said.ozcan.co',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
