from setuptools import setup, find_packages


setup(
    name="travisty",
    version="0.0.3",
    description="Repo for testing out travis",
    packages=find_packages(),
    author="Martin Hunt",
    author_email="mhunt@ebi.ac.uk",
    url="https://github.com/martinghunt/travisty",
    entry_points={"console_scripts": ["travisty = travisty.__main__:main"]},
    install_requires=["pyfastaq >= 3.14.0"],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
    ],
)
