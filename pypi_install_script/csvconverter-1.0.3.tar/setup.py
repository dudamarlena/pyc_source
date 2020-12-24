from setuptools import setup 

def readme():
	with open('README.md') as f:
		README = f.read()
	return README

setup(
	name="csvconverter",
	version="1.0.3",
	description="csvconverter for se211",
	long_description=readme(),
	long_description_content_type="text/markdown",
	url="https://github.com/yeggyseo/csvconverter-py",
	author="Yegeon Seo",
	author_email="yeggy.seo@gmail.com",
	license="MIT",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.7",
	],
	package=["csvconverter"],
	inclide_package_data=True,
	install_requires=[""],
	entry_points={
		"console_scripts": [
		"csvconverter-se211=csvconverter.main:main",
		]
	}
)