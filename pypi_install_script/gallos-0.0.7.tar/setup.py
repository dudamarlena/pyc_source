"""
"""
import setuptools

with open("README.md", "r") as RM:
    LONG_DESCRIPTION = RM.read()

setuptools.setup(
    name='gallos',
    version='0.0.7',
    description="A sample package",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/Stegallo/gallos",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)
