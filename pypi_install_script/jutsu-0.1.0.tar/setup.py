from setuptools import setup, find_packages

from jutsu import __version__


setup(
    name = "jutsu",
    version = ".".join(map(str, __version__)),
    license = "BSD",
    description = "HTTP library for asyncio.",
    author = "Dave Hall",
    author_email = "dave@etianen.com",
    url = "https://github.com/etianen/jutsu",
    packages = find_packages(),
    extras_require = {
        "dev":  [
            "nose",
            "coverage",
        ],
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Framework :: Django",
    ],
)