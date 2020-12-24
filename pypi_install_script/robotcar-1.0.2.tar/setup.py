from setuptools import setup, find_packages
import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'robotcar'))


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


a = (package for package in find_packages()
     if package.startswith('robotcar'))
print(find_packages())

setup(
    name="robotcar",
    version="1.0.2",
    description="robotcar simulator package for education",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="UCSD Robotic Lab",
    packages=[package for package in find_packages()
                if package.startswith('robotcar')],
    author_email="g5hwang@ucsd.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=[],
)
