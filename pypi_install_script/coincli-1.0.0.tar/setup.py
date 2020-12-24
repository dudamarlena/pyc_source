import pathlib
from setuptools import setup

# The text of the README file
README = open("coincli/README.md", "r").read();

# This call to setup() does all the work
setup(
    name="coincli",
    version="1.0.0",
    description="A Command-line Cryptocurrency Stats Tracker Utility",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/RestaurantController/coincli",
    author="RestaurantController",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["coincli"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "coincli=coincli.__main__:main",
        ]
    },
)