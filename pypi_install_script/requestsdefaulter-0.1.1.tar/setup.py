import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='requestsdefaulter',
    version='0.1.1',
    url='https://github.com/ONSdigital/requestsdefaulter',
    license='MIT',
    author='RAS Development Team',
    author_email='onsdigital@linux.co.uk',
    description='Small library to set default headers in requests',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
