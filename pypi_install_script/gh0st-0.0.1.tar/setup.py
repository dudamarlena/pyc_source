from setuptools import setup, find_packages

setup(
	name='gh0st',
	version='0.0.1',
	url="https://gitlab.com/pyrogue6/gh0st",
	download_url="https://gitlab.com/pyrogue6/gh0st/-/archive/0.0.1/gh0st-0.0.1.tar.gz",
	author="Sabrina Held",
	author_email="pyrogue6@gmail.com",
	classifiers=[
	"Development Status :: 1 - Planning",
	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
	"Environment :: Console :: Curses",
	"Intended Audience :: End Users/Desktop",
	"Topic :: Games/Entertainment :: Turn Based Strategy",
	"Topic :: Games/Entertainment :: Puzzle Games",
	"Programming Language :: Python :: 3.7",
	"Programming Language :: Python :: 3.8"
	],
	license="GPLV3",
	license_file="LICENSE",
	description='Top down stealth & hacking game',
	long_description=open("README.md","r").read(),
	long_description_content_type="text/markdown",
	keywords="stealth hacking puzzle game",
	python_requires='>=3',
	# packages=['gh0st'],
	packages=find_packages(),
	package_data = {
	    '': ['*.txt']
	    },
	entry_points={
		"console_scripts": ["gh0st = gh0st.__main__:main"]
	},
	install_requires=[]#"curses", "warnings", "pathlib"]
)
