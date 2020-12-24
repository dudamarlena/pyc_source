import setuptools


# with open("README.md", "r") as fh:
# 	long_description = fh.read()

long_description = "A useful kit makes flask more RESTful."


setuptools.setup(
	name = "flask-restkit",
	version="2019.10.25",
	auth="derick",
	author_email="13750192465@163.com",
	description=long_description,
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/suckmybigdick/flask-restkit",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	install_requires=[
		"setuptools==41.0.1",
	],
)



