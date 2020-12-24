from setuptools import setup, find_packages
import sys, os

version = '1.0.0'

setup(name='simple-pipeline',
      version=version,
      description="A simple data pipeline",
      long_description="""\
Data pipeline to handle multi-step flows of data sanitization, processing, and posting. Includes conditional branching and easily reused partial pipes.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='pipeline sanitization api processing',
      author='todamark',
      author_email='toda.mark@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
