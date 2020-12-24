from setuptools import setup, find_packages  # type: ignore
import os

thisdir = os.path.dirname(__file__)

with open(os.path.join(thisdir, "README.md")) as fh:
    long_desc = fh.read()

dev_requires = ["black"]
tests_require = ["pytest", "coverage", "pytest-cov", "mypy", "flake8", "tox"]
setup(
    name="wait-notify",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Batch job submission and management tool",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url="http://github.com/paulgessinger/wait-notify",
    author="Paul Gessinger",
    author_email="hello@paulgessinger.com",
    license="MIT",
    install_requires=[
        "click",
        "halo",
        "psutil",
        "python-pushover",
    ],
    tests_require=tests_require,
    extras_require={"dev": dev_requires, "test": tests_require, "ipython": ["ipython"]},
    entry_points={"console_scripts": ["wait-notify=wait_notify.cli:main"]},
    packages=find_packages("src"),
    package_dir={"": "src"},
)
