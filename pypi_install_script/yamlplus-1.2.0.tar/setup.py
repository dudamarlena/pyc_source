from setuptools import setup

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setup(setup_requires=['pbr'],
      python_requires='>=3.6',
      pbr=True,
      install_requires=[
          "pyyaml"
      ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      )
