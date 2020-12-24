import os, setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()


def createDataFiles(directory):
	excludes = ( '__pycache__' )
	result = []
	for root, folders, files in os.walk(directory):
		if not root.endswith(excludes):
			result += [(root, [os.path.join(root,f) for f in files])]
	return result
	# return [(root, [os.path.join(root,f) for f in files])
 #    	for root, folders, files in os.walk(directory)]


	# return [(root, [os.path.join(root,f) for f in files])
 #    	for root, folders, files in os.walk(directory)]



datafiles  = [('.', ['acme.py', 'acme.ini.default', 'CHANGELOG.md'])]
datafiles += createDataFiles('acme')
datafiles += createDataFiles('apps')
datafiles += createDataFiles('docs')
datafiles += createDataFiles('init')
datafiles += createDataFiles('webui')
datafiles += createDataFiles('tools/init.example')
datafiles += createDataFiles('tools/notificationServer')
datafiles += createDataFiles('tools/resourceTemplates')
print(datafiles)
setuptools.setup(

	# Application name:
	name='ACME oneM2M CSE',

	# Version number (initial):
	version='0.3.0',

	# Application author details:
	author='Andreas Kraft',
	author_email='onem2m@mheg.org',
	url='https://github.com/ankraft/ACME-oneM2M-CSE',

	# Packages
	#packages=['acme', 'acme/resources', 'acme/helpers', 'apps', 'docs'],
	packages = [],

	# Include additional files into the package
	include_package_data=False,
	data_files=datafiles,



	# Details
	#url="http://pypi.python.org/pypi/MyApplication_v010/",

	#
	license='BSD 3-Clause',
	description="An open source CSE Middleware for Education.",
	long_description=long_description,
	long_description_content_type='text/markdown',

	# Dependent packages (distributions)
	install_requires=[
		'flask', 'psutil', 'requests', 'tinydb'
	],
	keywords='onem2m cse framework',
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
	],

	python_requires='>=3.8'

)
