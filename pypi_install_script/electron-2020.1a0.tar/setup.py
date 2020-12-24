import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="electron",
    version="v2020.1.a",
    author="Sai Seshu Chadaram",
    author_email="seshu1729@outlook.com",
    description="A Python based Quantum Circuit Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seshu1729/electron",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
