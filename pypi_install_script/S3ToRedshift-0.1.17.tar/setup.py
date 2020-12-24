import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

module_version = "0.1.17"

setup(
    name="S3ToRedshift",
    packages=["S3ToRedshift"],
    version=module_version,
    license="MIT",
    description="Connector to upload csv/csv gzip file from S3 bucket into Redshift table.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samyak Ratna Tamrakar",
    author_email="samyak.r.tamrakar@gmail.com",
    url="https://github.com/srtamrakar/python-s3-to-redshift",
    download_url=f"https://github.com/srtamrakar/python-s3-to-redshift/archive/v_{module_version}.tar.gz",
    keywords=["aws", "s3", "redshift", "csv", "gzip"],
    install_requires=["pandas>=0.25.0", "GiantPandas>=0.2.0", "S3Connector>=0.2.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Database Engines/Servers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
