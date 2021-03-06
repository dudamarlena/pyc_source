import setuptools

with open("readme.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="DotMeme",
	version="0.2.4",
	author="Jake Leahy",
	author_email="darhyaust@gmail.com",
	description="A package to use .meme files",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitlab.com/ire4ever1190/dotmeme",
	packages=setuptools.find_packages(),
	include_package_data=True,
	install_requires=[
		'Pillow',
		'pyyaml',
		'requests'
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
