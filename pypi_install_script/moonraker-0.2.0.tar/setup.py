import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="moonraker",
    version="0.2.0",
    author="Brendan Samek",
    author_email="brendan@insidedesk.com",
    description="Package for simplifying interactions with aws and Docker for InsideDesk collection developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/InsideDesk/moonraker",
    packages=setuptools.find_packages(),
    install_requires=["logzero", "boto3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
