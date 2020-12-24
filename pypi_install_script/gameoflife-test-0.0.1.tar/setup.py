import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
                 name="gameoflife-test",
                 version="0.0.1",
                 author="lamdoanduc",
                 author_email="duclamsp@gmail.com",
                 description="An example package of lamdoanduc",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/lamdoanduc/game-of-life",
                 packages=setuptools.find_packages(),
                 classifiers=[
                              "Programming Language :: Python :: 3",
                              "License :: OSI Approved :: MIT License",
                              "Operating System :: OS Independent",
                              ],
                 )