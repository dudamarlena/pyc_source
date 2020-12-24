from distutils.core import setup

setup(
	name = 'Gifpy',
	version = '1.0',
	description = 'Portable and easy to use wrapper around the Giphy API',
	author = 'Iorga Dragos Florian',
	author_email = 'iorgadragos04@gmail.com',
	url = 'https://gitlab.com/IDF31/Gifpy',
	packages = ['gifpy'],
	scripts = ['bin/gifpy-upload']
)
