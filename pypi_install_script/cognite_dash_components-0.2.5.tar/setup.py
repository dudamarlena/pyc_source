import json
from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open("package.json") as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package["author"],
    author_email=package["authorEmail"],
    packages=[package_name],
    include_package_data=True,
    license=package["license"],
    description="Plotly Components for Cognite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=["Framework :: Dash"],
)
