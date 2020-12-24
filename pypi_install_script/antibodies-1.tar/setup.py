import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='antibodies',
    version='1',
    #packages=['antibodies',],
    description='Helpful Scripts for Antibody NGS Data Processing',
    author="CollinJ0",
    url= 'https://www.github.com/CollinJ0/antibodies',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=['bin/antibodies'],
    install_requires=[           
            'numpy',
            'pandas',
            'matplotlib',
            'seaborn',
            'pymongo',
            'tqdm',
            'abutils',
        ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)