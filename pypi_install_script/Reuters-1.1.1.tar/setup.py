import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Reuters",
    version="1.1.1",
    author="Hurin Hu",
    author_email="hurin@live.ca",
    description="Reuters ticker information retriever for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HurinHu/Reuters",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
