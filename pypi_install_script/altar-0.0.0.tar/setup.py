from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="altar",
    version="0.0.0",
    description="A suite of productivity tools with CLI and Urwid-based TUI interfaces.",
    long_description=long_description,
    url="https://github.com/lainproliant/altar",
    author="Lain Musgrove (lainproliant)",
    author_email="lainproliant@gmail.com",
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="notes todo urwid tui",
    packages=find_packages(),
    install_requires=["xeno>=3.0.0", "urwid"],
    entry_points={"console_scripts": ["altar=altar.tui:main"]},
)

