from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="ProxyGuysPy",
	version="1.1",
	author="Kurt Kobzeff",
	description="Python API for ProxyGuys",
	long_description=long_description,
	packages=['ProxyGuysPy']
)