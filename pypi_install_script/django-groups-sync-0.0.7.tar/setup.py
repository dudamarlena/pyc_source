import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-groups-sync",
    version="0.0.7",
    author="Jan Tezner",
    author_email="jan.tezner@gmail.com",
    description="A set of management commands to export and sync Django User Groups permissions between environments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hansek/django-groups-sync",
    license="License :: OSI Approved :: MIT License",
    packages=setuptools.find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[],
    scripts=[],
    entry_points={},
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
    ],
)
