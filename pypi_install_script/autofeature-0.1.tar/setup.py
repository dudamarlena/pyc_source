# from distutils.core import setup

import sys
from setuptools import setup, find_packages

setup(
	name='autofeature',
	version='0.1',
	license="",
	description="a library to automate feature engineering",
	author="Jing Y.",
	author_email='joyceye04@gmail.com',
	url="",
	download_url="",
	# packages=find_packages(exclude=['tests*']),
	packages = find_packages(),
	install_requires=[
		  "numpy",
		  "pandas"
	  ],
	keywords=[
		  "FeatureEngineering"
	  ]
)