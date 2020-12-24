from setuptools import setup
from os import path

pwd = path.abspath(path.dirname(__file__))

with open(path.join(pwd, 'sd-wan', 'README.md'), "r") as fh:
    long_description = fh.read()

setup(name='spirent-sdwan-test-suite',
      version='1.0',
      description='Spirent SD-WAN Functional Test Suite',
      maintainer='Spirent Testpack Development Team',
      maintainer_email='testpack@spirent.com',
      url='https://github.com/Spirent/SDWAN-Functional-Test-Suite',
      long_description = long_description,
      long_description_content_type="text/markdown",
      packages=['sd-wan'],
      package_data={'sd-wan': ['testbed_templates/*', 'testbed_lab/*', '*.yaml', '*.xml', '*.robot', '*.pdf', 'LICENSE', 'NOTICES', 'README.md']},
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: iOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.6",
        "Topic :: System :: Networking",
        "Topic :: System :: Benchmark",
        "Topic :: Software Development :: Testing :: Traffic Generation",
      ],
     )
