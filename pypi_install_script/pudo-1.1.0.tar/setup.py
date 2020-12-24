#!/usr/bin/python3
import setuptools
from setuptools.command.install	import install

import pudo


class PudoCmdInstall(install):
	def run(self):
		import os
		import sys
		from distutils.spawn import find_executable, spawn
		# check or install gcc
		if (not find_executable('gcc')):
			import pip
			if hasattr(pip, 'main'):
				pip.main(['install', 'gcc7'])
			else:
				pip._internal.main(['install', 'gcc7'])
		# compile and install pudo
		srcFile = 'pudo/pudo.c'
		spawn(cmd=('gcc', srcFile, '-o', pudo.PUDO_BINARY))
		install.run(self)


setuptools.setup(
    name='pudo', 
    version=pudo.VERSION,
    author='Madhusudhan Kasula',
    author_email='kasula.madhusudhan@gmail.com',
    description='Python version of linux sudo command without password prompt',
    long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/kasulamadhusudhan/pudo',
	data_files=[('bin', [pudo.PUDO_BINARY])],
	cmdclass={
		'install': PudoCmdInstall,
	},
	packages=setuptools.find_packages(),
	use_2to3=True,
	classifiers=[
		'Programming Language :: C',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2',
		'Operating System :: POSIX :: Linux',
		'Environment :: Console',
		'Intended Audience :: Developers',
	],
)
