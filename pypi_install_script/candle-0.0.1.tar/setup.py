# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(name='candle',
      version=VERSION,
      description='a machine learning scaffolding tool based on sklearn',
      long_description='a machine learning scaffolding tool based on sklearn',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='sklearn scaffold machine learning data mining',
      author='ver217',
      author_email='lhx0217@gmail.com',
      url='https://github.com/ver217/candle',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'numpy',
          'matplotlib',
          'scikit-learn'
      ],
      entry_points={
          'console_scripts': [
              'candle = candle.candle:main'
          ]
      },
      )
