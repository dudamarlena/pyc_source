import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
        name = "StatArbTools",
        version="0.0.5",
        author="Matthew Firth",
		packages=setuptools.find_packages(),
		py_modules=['StatArbTools'],
        author_email="mmf001x@yahoo.com",
        description="A set of tools useful in exploring statistical arbitrage",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/mattfirth7/StatArbTools",
        classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                ],
        python_requires='>=3.7',
        )