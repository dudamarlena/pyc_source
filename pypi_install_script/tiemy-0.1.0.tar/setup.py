
"""
Tiemy
--------

A minimalistic timing decorator for callables

Tiemy is timid
``````````````

::

    >>> from tiemy import timer
    >>> @timer
    >>> def function(*args):

easy to install
```````````````
::

    $ pip install tiemy

Links
`````

* `pypi <http://pypi.python.org/pypi/tiemy>`_
* `github repo <https://github.com/rahulunair/tiemy>`_

Latest Release Notes (version: 0.1.0)
`````````````````````````````````````

* one decorator `timer` to time functions and print mean and std of runs
"""

from distutils.core import setup

setup(name="tiemy",
    version="0.1.0",
    description="A minimalistic timing decorator for callables",
    long_description=__doc__,
    author="unrahul",
    author_email="mail@rahul.onl",
    license="three-clause BSD",
    url="http://github.com/rahulunair/tiemy",
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: System :: Benchmark "],
    py_modules=['tiemy'],)

