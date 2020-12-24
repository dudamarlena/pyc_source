from setuptools import setup

setup(
	name='savager',
    version='0.1',
    url="https://gitlab.com/pyrogue6/savager.git",
    download_url="https://gitlab.com/pyrogue6/savager/-/archive/0.1/savager-0.1.tar.gz",
	maintainer="Sabrina Held",
	maintainer_email="pyrogue6@gmail.com",
	classifiers=[
	"Development Status :: 1 - Planning",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python :: 3.7",
	"Programming Language :: Python :: 3.8",
	"Topic :: Multimedia :: Graphics",
	"Topic :: Artistic Software"
	],
    license="MIT License",
	license_file="LICENSE",
	description='create SVG files with python scripts',
    long_description=open("README.md","r").read(),
    long_description_content_type="text/markdown",
	keywords="svg",
    python_requires='>=3',
    packages=['savager'],
    install_requires=[]
)
