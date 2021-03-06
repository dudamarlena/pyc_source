import codecs
import os

from setuptools import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), 'rt').read()

setup(
	name = "pyRoblox",
	version = "0.0.3",
	description = "Python library for interfacing with Roblox",
	long_description = read("README.md"),
	url = "https://github.com/EchoReaper/pyroblox",
	author = "Drew Warwick",
	author_email = "dwarwick96@gmail.com",
	license = "Apache 2.0",
	packages = find_packages(exclude=["tests"]),
	install_requires = [
		"requests", "bs4", "python-dateutil"
	],
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Environment :: Web Environment",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3.6"
	]
)