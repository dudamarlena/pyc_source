from setuptools import setup, find_packages

from plusplusgael import __version__


with open("README.md", encoding="utf8") as f:
    readme = f.read()

setup(
    name="plusplusgael",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    description="plusplusgael test",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=[
        "tqdm==4.31.1"
    ],
    url="https://github.com/rundimeco/plusplusgael",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    license="MIT",
    entry_points={
        'console_scripts': [
            "plusplusgael = plusplusgael:plus_toto"
        ]
    }
)
