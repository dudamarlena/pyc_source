from distutils.core import setup

setup(
	name='django_compilers',
	packages=['compilers'],
	version='0.1',
	license='GNU GPL 3.0',
	description='This adds compilers for various static files, such as SASS.',
	author='Jonathan Leeming',
	author_email='jpleeming51@gmail.com',
	url='https://github.com/moddedTechnic/django-compilers',
	download_url='https://github.com/moddedTechnic/django-copmilers/archive/v0.1.1-alpha.tar.gz',
	keywords=['django', 'HTML', 'components'],
	install_requires=[],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Framework :: Django :: 3.0',
		'Topic :: Software Development',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.8',
	],
)
