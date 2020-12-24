import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="geokrety_api_exceptions",
    version="0.0.1",
    author="Mathieu Alorent",
    author_email="kumy@geokrety.org",
    description="The GeoKrety API Exceptions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geokrety/geokrety-api-exceptions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
