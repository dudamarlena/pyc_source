import setuptools


def read_reqs(path):
    with open(path, 'r') as fil:
        return list(fil.readlines())


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
)
