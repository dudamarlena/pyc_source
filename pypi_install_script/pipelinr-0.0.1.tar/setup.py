import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pipelinr",
    version="0.0.1",
    author="Guillaume Fe",
    author_email="guillaume.ferron@gmail.com",
    description="An effective task engine that displays only the next actionables tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guillaumefe/pipelinr",
    py_modules = ['pipelinr'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'pipelinr = pipelinr:main',
            ],
        },
    python_requires='>=3.6',
)
