from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
                name="adem-ademmy",
                version="1.0.0",
                author="Miracle Adebunmi",
                author_email="miraclem2014@gmail.com",
                description="Giving Python Ability to Work directly on Matrices",
                long_description=long_description,
                license = 'MIT',
                long_description_content_type="text/markdown",
                url="https://github.com/pypa/sampleproject",
                packages = find_packages(),
                classifiers = [
                                "Programming Language :: Python :: 3",
                                "License :: OSI Approved :: MIT License",
                                "Operating System :: OS Independent",
                              ],
                python_requires ='>=3.6',
                
)
