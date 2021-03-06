from setuptools import setup, find_packages
import sys

setup(
    name="spinnaker_proxy",
    version="2.0.4",
    packages=[],
    scripts=["spinnaker_proxy/spinnaker_proxy.py"],

    # Metadata for PyPi
    author="Jonathan Heathcote",
    description="A proxy-server for SpiNNaker systems.",
    license="GPLv2",
    url="https://github.com/SpiNNakerManchester/spinnaker_proxy",

    # Requirements
    install_requires=["six"],
)
