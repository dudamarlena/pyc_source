import setuptools
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="edf-pystore",
    version="4.0.9",
    author="Léo Richard",
    author_email="leo-externe.richard@edf.com",
    description="Un connecteur python pour authentifier et autoriser des utilisateurs "
                "sur les applications de l'HydroStore.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/leogout/edf-pystore",
    packages=setuptools.find_packages(include=('pystore',)),
    install_requires=[
        "authlib",
        "requests",
        "python-decouple",
    ],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
)
