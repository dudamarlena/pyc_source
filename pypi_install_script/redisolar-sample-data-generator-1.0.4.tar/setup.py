import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as reqs:
    install_requires = reqs.read()

with open("requirements-dev.txt", "r") as reqs:
    dev_requires = reqs.read()

setuptools.setup(
    name="redisolar-sample-data-generator",
    version="1.0.4",
    author="Andrew Brookins",
    author_email="andrew.brookins@redislabs.com",
    description="A sample data generator for Redis University's example application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redislabs-training/redisolar-sample-data-generator/",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
    include_package_data=True,
    extras_require={
        "dev": dev_requires
    },
    entry_points={
        "console_scripts": [
            "load_redisolar = sample_data_generator.main:load"
        ]
    }
)
