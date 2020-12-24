import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="AutoDifferentiate",
                 version="1.0.1",
                 author="Lihong Zhang, Yichen Geng, Yingsi Jian, Matthieu Meeus  ",
                 description="An AutoDifferentiation package",
                 long_description="The software library uses the concept of automatic differentiation "
                                  "to solve differentiation problems in scientific computing. Additional"
                                  " features of an optimization suite and a root finding suite are also "
                                  "listed in this documentation.",
                 long_description_content_type="text/markdown",
                 url="https://github.com/BackPropagators/cs207-FinalProject.git",
                 packages=setuptools.find_packages(),
                 install_requires =['certifi == 2019.9.11', 'wincertstore == 0.2', 'numpy==1.17.4'],
                 classifiers=[
                              "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )
