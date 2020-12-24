from setuptools import setup

with open("README.md") as readme:
    long_description = readme.read()


setup(
    name="girder-ess-dive",
    version="1.0.1",
    description="Allows access to ESS-DIVE files through a read-only assetstore.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/girder/girder-ess-dive",
    packages=["girder_ess_dive"],
    python_requires=">=3.5",
    install_requires=[
        "girder",
        "pytest",
        "requests",
        "xmltodict",
        "shapely",
        "pyproj",
    ],
    entry_points={"girder.plugin": ["ess-dive = girder_ess_dive:GirderESSDive"]},
)
