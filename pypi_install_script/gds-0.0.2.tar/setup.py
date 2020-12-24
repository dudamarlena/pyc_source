#!/usr/bin/env python
from setuptools import setup, find_packages

exec(open("gds/__version__.py").read())
github_page = 'https://github.com/guidanoli/gds'

setup(
	name='gds',
	description='A collection of well known data structures'
				' implemented in Python.',
	keywords = ['data structures', 'graph'],
	author='Guilherme Dantas',
	author_email='guidanoli@hotmail.com',
	url=github_page,
	download_url=github_page+'/archive/'+__version__+'.tar.gz',
	license='MIT',
	
	packages=["gds"],
	version=__version__,
	long_description=open('README.rst').read(),
	
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
)

