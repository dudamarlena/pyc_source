from setuptools import setup

setup(
	name='py-orgmanager-api',
	version='1.0.0',
	description='A Python client for the OrgManager API',
	packages=['orgmanager'],
	author = 'OrgManager',
	license = 'MPL',
	url = 'https://github.com/orgmanager/py-orgmanager-api',
	install_requires= [
		'requests'
	],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
		'Natural Language :: English',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.0',
		'Programming Language :: Python :: 3.1',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Internet',
		'Topic :: Utilities',
	],
	keywords = 'orgmanager'
)
