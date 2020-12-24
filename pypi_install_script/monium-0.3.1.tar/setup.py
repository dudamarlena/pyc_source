from setuptools import setup, find_packages

from monium import __title__, __version__, __author__, __license__


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name=__title__,
    version=__version__,
    description="Discord Bot Framework",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="discord bot framework discord.py modular",
    url="https://github.com/monium-project/monium",
    author=__author__,
    author_email="me@ecmelberk.com",  # todo: change when we get a proper domain.
    license=__license__,
    packages=find_packages(),
    install_requires=["discord.py", "pyhocon"],
    extras_require={"voice": ["PyNaCl", "youtube_dl"]},
    scripts=["bin/monium", "bin/monium.bat"],
    include_package_data=True,
    test_suite="nose.collector",
    tests_require=["nose"],
    zip_safe=False,
)
