from setuptools import setup

setup(
	name='unicorn_banner',
	version=0.1,
	description='Display text as a banner on a Unicorn Hat device',
	url='https://bitbucket.org/marrem/raspi-unicornhat-banner/src/master/',
	author='Marc Remijn',
	author_email='software@dubhead.org',
	license='GPL',
	packages=['unicorn_banner'],
	install_requires=['unicornhat','pyfiglet'],
	zip_safe=False,
	test_suite='nose.collector',
	tests_require=['nose']
)


