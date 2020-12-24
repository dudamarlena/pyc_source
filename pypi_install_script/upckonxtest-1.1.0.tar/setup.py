import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upckonxtest", 
    version="1.1.0",
    author="MoriartyYang",
    author_email="moriarty0305@icloud.com",
    description="A simple printer of nested lists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://moriartyyang.top",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
) 