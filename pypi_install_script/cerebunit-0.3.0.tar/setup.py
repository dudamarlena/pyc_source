# ~/cerebtests/setup.py
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
        name="cerebunit",
        version="0.3.0",
        author="Lungsi",
        author_email="lungsi.sharma@unic.cnrs-gif.fr",
        #packages=find_packages(),
        packages=["cerebunit",
                  #"cerebunit.file_manager",
                  #"cerebunit.test_manager",
                  "cerebunit.statistics",
                  "cerebunit.statistics.data_conditions",
                  "cerebunit.statistics.stat_scores",
                  "cerebunit.statistics.hypothesis_testings",
                  # capabilities 
                  "cerebunit.capabilities",
                  "cerebunit.capabilities.cells",
                  # validation_tests
                  "cerebunit.validation_tests",
                  "cerebunit.validation_tests.cells",
                  #"cerebunit.validation_tests.cells.general",
                  "cerebunit.validation_tests.cells.Purkinje",
                  "cerebunit.validation_tests.cells.Granule",
                  #"cerebunit.validation_tests.cells.GolgiCell"
                  ],
        url="https://github.com/cerebunit/cerebtests",
        download_url = "https://github.com/cerebunit/cerebtests/archive/v0.3.0.tar.gz",
        keywords = ["VALIDATION", "CEREBELLUM", "NEUROSCIENCE",
                    "MODELING", "SCIENTIFIC METHOD"],
        license="BSD Clause-3",
        description="Installable package 'cerebtest' for cerebunit",
        long_description="",
        install_requires=[
            "sciunit",
            "quantities",
            "scipy",
            "numpy",
            ],
        classifiers = [
            # "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as current state of package
            "Development Status :: 4 - Beta",
            # Define audience
            "Intended Audience :: Developers",
            # License
            "License :: OSI Approved :: BSD License",
            # Specify supported python versions
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            ],
)
