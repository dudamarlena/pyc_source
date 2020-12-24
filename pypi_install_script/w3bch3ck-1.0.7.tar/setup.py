from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='w3bch3ck',
    version='1.0.7',
    packages=find_packages(exclude=['unittests*', ]),
    package_dir={'w3bch3ck': 'w3bch3ck'},
    author='Anzhela',
    author_email='dev.anzhela@gmail.com',
    description="Package for primary check for web service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)
