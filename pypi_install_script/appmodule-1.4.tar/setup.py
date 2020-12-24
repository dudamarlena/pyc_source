from distutils.core import setup

setup(
    # Application name:
    name="appmodule",

    # Version number (initial):
    version="1.4",

    # Application author details:
    author="ganesh",
    author_email="ganesh@gmail.com",

    # Packages
    packages=["appmodule"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    #url="http://pypi.python.org/pypi/appflask.0.1/",

    #
    license="LICENSE.txt",
    description="Useful towel-relathjadsfkjasfjkasdfed stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
	"flask",
    "twisted"]
)
