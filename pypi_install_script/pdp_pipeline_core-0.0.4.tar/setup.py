import os
from setuptools import setuptools


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="pdp_pipeline_core",
    version="0.0.4",
    author="sai krishna",
    author_email="v_lakkoju@spglobal.com",
    description=("A module for handling core functionalities like kafka, logging and repository"),
    package_dir={'pdp_pipeline_core': 'src'},
    # packages=setuptools.find_packages(),
    # packages=setuptools.find_packages(include=['pdp_pipeline_core', 'pdp_pipeline_core.*']),
    packages=['pdp_pipeline_core', 'pdp_pipeline_core.core', 'pdp_pipeline_core.pdp_kafka',
              'pdp_pipeline_core.repository', "pdp_pipeline_core.Utils", "pdp_pipeline_core.pdp_kafka.consumer",
              "pdp_pipeline_core.pdp_kafka.producer"],

    install_requires=[
        # 'watchtower', 'PyYAML'
    ]
)
