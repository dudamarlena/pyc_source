# TODO: Fill out this file with information about your package

# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
# from setuptools import setup

# setup(name='distributions',
#       version='0.1',
#       description='Gaussian distributions',
#       packages=['distributions'],
#       zip_safe=False)

import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="AlgebraOnMatrix",
    version="0.0.1",
    author="Prerana",
    author_email="prerana.gawale@gmail.com",
    description="Algebric operations on matrices",
    long_description="This package does basic matrix algebra such as addition, subtraction, multiplication, transpose of matrix.",
#     long_description_content_type="text/markdown",
    url="https://github.com/preranagawale/portfolio_test1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)