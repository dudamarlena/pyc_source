import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msSmartHome", 
    version="0.0.1",
    author="MS",
    author_email="",
    description="smart home package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/michemil/mssmarthome",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)