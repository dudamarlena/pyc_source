from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
	long_description = f.read()

setup(
	name="nhentai.py",
	version="1.0.5",
	packages=['nhentai'],
	author="moka",
	description='an nhentai api wrapper (using beautifulsoup)',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/moe-ka/nhentai.py',
	include_package_data=True
)