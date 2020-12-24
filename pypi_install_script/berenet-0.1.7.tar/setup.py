from distutils.core import setup

setup(
	name = 'berenet',
	packages = ['berenet'],
	version = '0.1.7',
	license='MIT',
	description = 'Simple matrix based neural network library.',
	author = 'Daniel Berezovski',
	author_email = 'danieldaniber@gmail.com',
	url = 'https://github.com/Shoop123/berenet',
	download_url = 'https://github.com/Shoop123/berenet/archive/0.1.7.tar.gz',    # I explain this later on
	keywords = ['machine learning', 'neural network', 'feed forward', 'recurrent'],
	install_requires=[
		'numpy',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)