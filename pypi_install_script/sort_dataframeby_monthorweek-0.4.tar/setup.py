import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sort_dataframeby_monthorweek",
    version="0.4",
    author="Yeddu Dinesh Babu",
    author_email="ydineshy225@gmail.com",
    description="Sort a dataframe by month name or by weekday name in chronological order",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ydineshy225/sort-dataframeby-monthorweek",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)