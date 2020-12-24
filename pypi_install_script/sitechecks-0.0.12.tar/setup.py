from setuptools import setup, find_packages


with open("README.md") as f:
    long_description = f.read()

requirements = (
    "requests",
    "click",
    "cachecontrol",
    "beautifulsoup4",
    "structlog",
    "jinja2",
    "marshmallow",
    "pyyaml",
)

setup(
    name="sitechecks",
    version="0.0.12",
    description="A no-nonsense set of best-practices for public HTML marketing websites.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dropseed",
    author_email="python@dropseed.io",
    python_requires=">=3.6.0",
    url="https://github.com/dropseed/sitechecks",
    packages=find_packages(exclude=("tests", "docs")),
    entry_points={"console_scripts": ["sitechecks=sitechecks.cli:cli"]},
    install_requires=requirements,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
