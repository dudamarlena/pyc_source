import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="PyMitmProxy",
	version="0.0.1",
	author="Format_HDD",
	author_email="formathdd.yt@gmail.com",
	description="A TCP Proxy creation lib for interactive manipulating and handling TCP packages.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/FormatHDD/PyMitmProxy",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
