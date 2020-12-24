#!/usr/bin/env python
try:
    from setuptools import setup, Command
    kwargs = {"zip_safe": False}
except ImportError:
    from distutils.core import setup, Command
    kwargs = {}
from sqmedium import version

class test (Command):
    description="Run test suite"

    user_options=[
        ("verbosity", "v", "Increase verbosity"),
        ]
    def initialize_options(self):
        for i in map (lambda i: i [0], self.user_options):
            setattr (self, i, None)

    def finalize_options(self):
        pass
    
    def run(self):
        self.verbosity = int(bool(self.verbosity))+1
        kwargs = {}
        for i in map (lambda i: i [0], self.user_options):
            kwargs [i] = getattr (self, i)
        from sqmedium import test
        test (**kwargs)

setup ( # Distribution meta-data
        name = "sqmediumlite",
        version = version,
        description = "Python SQLite tools",
        long_description="""Programming tools for Pythop SQLite""",
        author = "Edzard Pasma",
        author_email = "pasma10@concepts.nl",
        license = "Open Source",
        platforms = "ALL",
        url = "",
        # Description of the modules and packages in the distribution
        package_dir={
            'sqmedium':'sqmedium',
            },
        packages = [
            "sqmedium",
            ],
        scripts = [
            ],
        data_files = [
            ###('.', (
            ###    'README.txt',
            ###    'index.html',
            ###    ###'setup.py', # comes from argv [0]
            ###    )),
            ],
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: zlib/libpng License",
            "Programming Language :: Python",
            "Topic :: Database :: Database Engines/Servers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Communications :: File Sharing"],
        cmdclass={
            'test': test,
             },
        **kwargs
        )

