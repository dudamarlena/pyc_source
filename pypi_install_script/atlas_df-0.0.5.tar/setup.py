import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="atlas_df",
    version="0.0.5",
    author="Maxime Mouchet",
    author_email="max@maxmouchet.com",
    description="A dataframe-oriented interface to RIPE Atlas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxmouchet/atlas_df",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    # TODO: Pin versions
    install_requires=[
        "ripe.atlas.cousteau",
        "pandas",
        "geopandas"
    ]
)
