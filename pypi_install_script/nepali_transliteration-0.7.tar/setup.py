import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nepali_transliteration',
    version='0.7',
    author="Santosh Dahal",
    author_email="dahalsantosh2018@gmail.com",
    description="Convert roman English to Nepali text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/santoshdahal2016/nepali-transliteration",
    packages=setuptools.find_packages(),
    py_modules=["nepali-transliteration"],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
)
