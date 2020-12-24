import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonanywhere_test_package",
    version="0.0.2",
    author="PythonAnywhere Developers",
    author_email="developers@pythonanywhere.com",
    description="A package for testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pythonanywhere/pythonanywhere_test_package",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)