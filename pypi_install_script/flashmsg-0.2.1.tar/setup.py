
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='flashmsg',
     version='0.2.1',
     scripts=['flashmsg.py'],
     author="Daniel C. Baeriswyl",
     author_email="daniel@magic-carpet.ch",
     description="A fancy print",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/baeriswyld/flash_msg",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )