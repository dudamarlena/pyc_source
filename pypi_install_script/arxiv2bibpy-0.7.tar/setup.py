import os
import setuptools

cwd = os.path.abspath(os.path.dirname(__file__))

with open(cwd + "/requirements.txt") as f:
    requirements = f.read().split("\n")

with open(cwd + "/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version="0.7",
    include_package_data=True,
    name="arxiv2bibpy",
    author="Duong Nhu",
    author_email="d.binhnhu@gmail.com",
    description="Search arxiv via api and save as bib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="arxiv, bibtext, bib",
    url="https://github.com/code-fury/arxiv2bib",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    scripts=["arxiv2bib/arxiv2bib"],
    license="MIT",
)
