import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
      name='postnlpy',
      version='0.4.1',
      description='Python wrapper for the PostNL API, a way to retrieve your packages and letters',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://www.github.com/peternijssen/postnlpy/',
      author='Peter Nijssen',
      author_email='peter@peternijssen.nl',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=setuptools.find_packages(),
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
      ),
)