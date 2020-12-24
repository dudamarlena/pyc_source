# pyRIST. Copyright 2019-2020 Mad Resistor LLP. All right reserved.
# Author: Kuldeep Singh Dhaka <kuldeep@madresistor.com>

from setuptools import setup, find_packages
import os, io, re

# https://python-packaging-user-guide.readthedocs.io/single_source_version/

def read(*names, **kwargs):
	path = os.path.join(os.path.dirname(__file__), *names)
	encoding = kwargs.get("encoding", "utf8")
	with io.open(path, encoding=encoding) as fp:
		return fp.read()

def find_version(*file_paths):
	version_file = read(*file_paths)
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
							version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError("Unable to find version string.")

def find_requirements():
	with open('requirements.txt') as f:
		return f.read().splitlines()

setup(
	name = 'rist',
	version = find_version('rist', '__init__.py'),
	author = 'Kuldeep Singh Dhaka',
	author_email = 'kuldeep@madresistor.com',
	description = ('librist Binding'),
	license = 'BSD 2-Clause "Simplified" License',
	keywords = 'RIST librist reliable video stream',
	url = 'https://code.videolan.org/rist/pyrist',
	long_description = read('README.md'),
	long_description_content_type = 'text/markdown',
	packages = find_packages(include='rist.*'),
	install_requires = find_requirements(),
	classifiers = [
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: BSD License',
		'Topic :: Scientific/Engineering'
	]
)

