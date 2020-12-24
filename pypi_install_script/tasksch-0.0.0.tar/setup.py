import os

import setuptools

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name="tasksch",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="AP Ljungquist",
    author_email="ap@ljungquist.eu",
    description="A tiny library for easing into some modern asyncio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/apljungquist/tasksch",
    packages=setuptools.find_packages('tasksch'),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
