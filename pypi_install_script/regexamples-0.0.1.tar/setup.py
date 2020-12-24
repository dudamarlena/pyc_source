import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="regexamples",
    version="0.0.1",
    author="Abarad",
    author_email="alon710@gmail.com",
    description="A regex examples package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abarad/python-regex-examples",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
