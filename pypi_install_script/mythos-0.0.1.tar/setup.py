import os

from codecs import open

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

name = "mythos"
url = "https://github.com/theyarek/mythos"

about = {}
with open(os.path.join(here, name, "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)


setup(
    name=name,
    version=about["__version__"],
    description=about["__description__"],
    long_description=about["__description__"],
    author=about["__author__"],
    license=about["__license__"],
    url=url,
    packages=[name],
    package_data={},
    package_dir={name: name},
    include_package_data=True,
    python_requires=">=3.6.0",
    install_requires=[],
    extras_require={
        "dev": [
            "pycodestyle", "flake8", "mypy",
            "coverage", "pytest", "pytest-cov"
        ]
    },
    tests_require=[],
    cmdclass={},
    entry_points={},
    zip_safe=False
)
