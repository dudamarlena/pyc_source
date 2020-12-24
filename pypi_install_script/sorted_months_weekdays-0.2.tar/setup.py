import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sorted_months_weekdays",
    version="0.2",
    author="Yeddu Dinesh Babu",
    author_email="ydineshy225@gmail.com",
    description="Get sorted Months and Weeks by chronological order",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ydineshy225/sorted-months-weekdays",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)