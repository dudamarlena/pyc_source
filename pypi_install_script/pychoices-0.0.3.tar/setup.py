from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pychoices",
    version="0.0.3",
    author="Breno Gomes",
    author_email="brenodega28@gmail.com",
    description="Small Python library for receiving choice input from user.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/brenodega28/pychoices",
    packages=find_packages(),
    install_required=[
        "cursor",
        "pynput"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)