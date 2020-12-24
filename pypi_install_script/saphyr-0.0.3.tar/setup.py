import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="saphyr",
    version="0.0.3",
    author="Guillaume Bailleul",
    author_email="laibulle@gmail.com",
    description="An experiemental fullstack framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laibulle/saphyr",
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['saphyr=saphyr.__main__:main',
                                      ]},
    classifiers=(
        'Development Status :: 1 - Planning',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),
)
