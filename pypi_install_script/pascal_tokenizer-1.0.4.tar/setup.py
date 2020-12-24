from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='pascal_tokenizer',
    version='1.0.4',
    packages=find_packages(),
    long_description=long_description,
    author='Artem Gavrilov',
    author_email='info@teamfnd.ru',
    url='',
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)