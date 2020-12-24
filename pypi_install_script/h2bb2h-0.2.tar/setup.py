from setuptools import setup, find_packages  

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
     name='h2bb2h',
     version='0.2',
     packages = find_packages(),
     author="Samarth Tripathi",
     author_email="samarthtripathi@gmail.com",
     description="Human to Byte , Byte to Human",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Samarth-Tripathi/h2bb2h",
 )
