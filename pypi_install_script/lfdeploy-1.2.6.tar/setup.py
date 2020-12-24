import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lfdeploy",
    version="1.2.6",
    author="Przemyslaw Winszczyk",
    author_email="n3onix@gmail.com",
    description="Improved tfdeploy module",
    url="https://github.com/LendFlo/Lendflo-tfdeploy",
    packages = ['lfdeploy'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)