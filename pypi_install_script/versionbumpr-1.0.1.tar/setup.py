import os
from setuptools import setup

with open(os.path.abspath("./README.md"), "r") as readme:
	long_description = readme.read()

setup(
	name="versionbumpr",
	version="1.0.1",
	description="Bump your setup.py's release version.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/jalavosus/versionbumpr",
	author="jalavosus",
	author_email="alavosus.james@gmail.com",
	license="MIT",
	packages=["versionbumpr"],
	zip_safe=False,
	entry_points = {
  	"console_scripts": ["versionbumpr=versionbumpr.commandline:main"],
	}
)