import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent



# This call to setup() does all the work
setup(
    name="pyfdownloader",
    version="1.0.0",
    description="Download files easily from the web",
    long_description_content_type="text/markdown",
    author="RestaurantController",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pydownload"],
    include_package_data=True,
    install_requires=["requests"],
)