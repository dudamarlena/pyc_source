import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ahmed M. Gamaleldin",
    version="0.0.1",
    author="Ahmed Gamaleldin",
    author_email="ahmedgamal1496@gmail.com",
    description="Package for Gaussian and Bionomial Distributions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
