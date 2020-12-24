from distutils.core import setup

setup(
    # Application name:
    name = "EINSTEIN",

    # Version number (initial):
    version = "1.0.0",

    # Application author details:
    author= "Mohd Wasih",
    author_email = "wasih.mohd@gmail.com",

    # Packages
    packages = ["EINSTEIN"],

    # Include additional files into the package
    include_package_data = True,

	package_data={
        'Fun1':
             ['Fun1/add.py',
             ],
        'Fun2':
            ['Fun2/subt.py',
            ],
    },
    # Details
    url="http://pypi.python.org/pypi/EINSTEIN_v100/",

    #
    # license="LICENSE.txt",
    description = "Useful speech recognition and transcription related library for Indian languages.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
    ],
)
