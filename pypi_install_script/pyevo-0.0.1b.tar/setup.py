import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pyevo",
    version="0.0.1",
    author="Tibor Eszes",
    author_email="teszes@protonmail.com",
    description="Package for applying evolutionary algorithms to various problem models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teszes/pyevo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Typing :: Typed"
    ],
    python_requires='>=3.6',
)

