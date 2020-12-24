import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cty_pkg",
    version="0.0.1",
    author="Tahiri Alaoui Omar",
    author_email="o.tahirialaoui@gmail.com",
    description="A small example package",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)