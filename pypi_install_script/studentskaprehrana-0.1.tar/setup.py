from setuptools import setup

setup(name = 'studentskaprehrana',
	version = '0.1',
	description = 'Scraper for studentska-prehrana.si website.',
	url = 'https://github.com/drobilc/studentskaprehrana',
	author = 'Niki Bizjak',
	author_email = 'drobilc@gmail.com',
	license = 'MIT',
	packages = ['studentskaprehrana'],
	zip_safe = False,
	download_url = 'https://github.com/drobilc/studentskaprehrana/archive/0.1.tar.gz',
	install_requires = [
		"requests",
		"beautifulsoup4"
	])