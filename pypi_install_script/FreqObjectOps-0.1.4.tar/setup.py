import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

module_version = "0.1.4"

setup(
    name="FreqObjectOps",
    packages=["FreqObjectOps"],
    version=module_version,
    license="MIT",
    description="Some special functions for some python objects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samyak Ratna Tamrakar",
    author_email="samyak.r.tamrakar@gmail.com",
    url="https://github.com/srtamrakar/python-general-functions",
    download_url=f"https://github.com/srtamrakar/python-general-functions/archive/v_{module_version}.tar.gz",
    keywords=["list", "string", "datetime", "directory", "path"],
    install_requires=["pandas>=0.25.0", "pytest>=5.0.1", "Unidecode>=1.0.22"],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Either"3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
