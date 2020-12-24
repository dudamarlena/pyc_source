import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datetime_extractor",
    version="0.5",
    author="Yeddu Dinesh Babu",
    author_email="ydineshy225@gmail.com",
    description="Extracts timestamp from a given text/string",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ydineshy225/datetime_extractor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)