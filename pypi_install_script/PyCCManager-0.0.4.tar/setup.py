import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCCManager",
    version="0.0.4",
    author="Camden Weaver",
    author_email="camden7306@gmail.com",
    description="Manage Geometry Dash game files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyCrypto'
    ],
    python_requires='>=3.7',
)