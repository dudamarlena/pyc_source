from distutils.core import setup

setup(
	name = 'plenum',
	packages = ['plenum'],
	version = '1.0',
	license = 'agpl-3.0',
	description = 'Plenum is a simple module for Artificial Neural Networks.',
	author = 'DeBruss',
	author_email = "stefbrusselers2000@gmail.com",
	url = 'https://github.com/debruss/plenum',
	download_url = 'https://github.com/debruss/plenum/archive/v1.0.tar.gz',
	keywords = ['Neural', 'Artificial', 'Network', 'AI'],
	install_requires=[
		'numpy',
	],
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',      # Define that your audience are developers
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',   # Again, pick a license
		'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	]
	)
