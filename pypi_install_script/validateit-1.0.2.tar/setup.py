import io
from setuptools import setup, find_packages

with io.open("README.rst", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="validateit",
    version="1.0.2",
    url="https://github.com/DamlaAltun/ValidateIt",
    license="MIT",
    author="Damla Altun",
    author_email="initalize.damla@gmail.com",
    maintainer="Damla Altun",
    maintainer_email="initalize.damla@gmail.com",
    description="Dataclasses Validators",
    long_description=readme,
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
