import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="levne",
    version="0.0.1",
    author="Christian Šidák",
    description="A python package for Amino Acid Clustering. Published February 2020",
    url="https://github.com/Christian-Sidak/levne.git",
    packages=['levne'],
    install_requires=[
        'sklearn',
        'matplotlib',
        'numpy',
        'pandas',
        'editdistance',
        'umap-learn',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
