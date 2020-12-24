import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="single-variable-expression-parser-ALIEZZAT",
    version="0.0.2",
    author="ALIEZZAT ODEH",
    author_email="aliezzat1993@outlook.com",
    description="A package for parsing mathmatical expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AliEzzatOdeh/SingleVariableExpressionParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
    ],
    python_requires='>=3.6',
)