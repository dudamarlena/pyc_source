#Import the “setup” function from Python’s distribution utilities.
from distutils.core import setup

setup(
	#These are the setup function’s argument names.
	name	= 'nester_wsebas',
	version = '1.3.0',
	py_modules = ['nester_wsebas'],
	author = 'wsebas9',
	author_email = 'wsebasvb@hotmail.com',
	description = 'A simple printer of nested lists',
	)