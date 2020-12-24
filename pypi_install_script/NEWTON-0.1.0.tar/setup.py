from distutils.core import setup

setup(
    # Application name:
    name = "NEWTON",

    # Version number (initial):
    version = "0.1.0",

    # Application author details:
    author= "Mohd Wasih",
    author_email = "wasih.mohd@gmail.com",

    # Packages
    packages = ["NEWTON"],

    # Include additional files into the package
    include_package_data = True,

    # Details
    url="http://pypi.python.org/pypi/ARISPLAT_v010/",

    #
    # license="LICENSE.txt",
    description = "Useful speech recognition and transcription related library for Indian languages.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
		
    ],
)
