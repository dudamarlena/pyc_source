import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhpipam",
    version="1.0.1.post1",
    author="Leo Kirchner",
    author_email="leo.kirchner@cgi.com",
    description="A Python API Client for PHPIPAM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kircheneer/pyhpipam",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests"
    ],
    extra_require={
        'dev': [
            'pytest'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
