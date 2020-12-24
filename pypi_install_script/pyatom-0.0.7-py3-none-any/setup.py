import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pyatom',
     version='0.0.4',
     author="Peng Xiong",
     author_email="xiongpengnus@gmail.com",
     description="Python Algebraic Toolbox for Optimization Modeling",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/XiongPengNUS/pyatom",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )
