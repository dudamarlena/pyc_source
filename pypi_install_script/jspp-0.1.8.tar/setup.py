from setuptools import setup
from setuptools import setuptools

def readme():
	with open('README.md') as blahblahblah:
		return blahblahblah.read()

setup(name="jspp",
	  version="0.1.8",
	  description="BETA",
	  long_description=readme(),
	  long_description_content_type="text/markdown",
	  classifiers=[
		  "Programming Language :: Python :: 3",
	  ],
	  url="https://github.com/JhinScripter/jspp",
	  packages=setuptools.find_packages(),
	  python_requires='>=3.6'
	)