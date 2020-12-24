import setuptools

def parse_readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description

setuptools.setup(
  name='parst',
  version='1.1.6',
  author='Max Bussiere',
  author_email='max.bussiere@gmail.com',
  description=parse_readme(),
  url='https://github.com/bussierem/parst/',
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ],
  scripts=['parst.py']
)
