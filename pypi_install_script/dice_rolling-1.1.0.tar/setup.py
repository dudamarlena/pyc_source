import pathlib

from setuptools import find_packages
from setuptools import setup

from dice_rolling import __version__

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="dice_rolling",
    version=__version__,
    description="Module to roll multiple dice.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ajordat/dice_roller",
    author="Ajordat",
    author_email="alexjortri@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7"
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "roll=dice_rolling.main:main"
        ]
    }
)
