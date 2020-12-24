import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="turkishfullnamegenerator", 
    version="0.0.5",
    author="anilkay",
    author_email="aanilkay@gmail.com",
    description="Generate full turkish names ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anilkay/Turkish-FullName-Generator",
    packages=["turkishfullname"],
    keywords = ['name generator', 'turk', 'turkish'], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)