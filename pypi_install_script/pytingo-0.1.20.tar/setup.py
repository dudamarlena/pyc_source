# -*- coding: utf-8 -*-


from distutils.core import setup


setup(
    name="pytingo",
    packages=["pytingo"],

    install_requires=[
        "six>=1.7.3"
    ],

    version="0.1.20",

    license="MIT",
    description="Settings Loader, Container and Manipulator.",

    author="Andrés Correa Casablanca",
    author_email="castarco@gmail.com",

    url="https://github.com/castarco/pytingo",
    download_url="https://github.com/castarco/pytingo/tarball/0.1.20",

    keywords=["settings", "json"],

    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: POSIX",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Installation/Setup"
    ]
)
