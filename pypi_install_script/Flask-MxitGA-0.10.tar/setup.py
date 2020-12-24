from setuptools import setup

setup(
	name='Flask-MxitGA',
	version='0.10',
	licence='MIT',
	author='Pierre Hugo',
	author_email='avoid3d@gmail.com',
	description='Google analytics for flask and mxit.',
	long_description=__doc__,
	packages=['flask_mxit_ga'],
	zip_safe=False,
	include_package_data=True,
	platforms='any',
	install_requires=[
		'Flask',
		],
	)
