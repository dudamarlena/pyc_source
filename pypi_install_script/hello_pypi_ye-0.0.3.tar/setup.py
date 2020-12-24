#！ /usr/bin/env python


from setuptools import setup

setup(
	name  = 'hello_pypi_ye',
	version = '0.0.3',
	description = 'this is a sample project for pypi upload test',
	url = 'https://pypi.org',
	keywords = 'sample upload pypi',
	author = 'YE',
	author_email  = 'xxx@qq.com',
	install_requires = [],
	entry_points = {
		'console_scripts':[
			'hello1=hello_pypi_ye:hello',
			'pypi1=hello_pypi_ye:pypi'
		]
	}
)
