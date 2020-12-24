from setuptools import setup
from pathlib import Path

source_root = Path(".")

setup(
    name = 'dsbox',
    packages = ['dsbox'],
    version = 'v0.0.1',  # Ideally should be same as your GitHub release tag varsion
    description = '',
    author = 'Kedar Dabhadkar',
    author_email = 'kdabhadk@gmail.com',
    url = 'https://github.com/dkedar7/dsbox',
    keywords = ['Data Science', 'Machine Learning'],
    python_requires='>=3',
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "*.rst"]},
    include_package_data=True,
    classifiers=[
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires = ['scipy>=1.4.1',
'matplotlib==3.2.0',
'seaborn',
'pandas-profiling']
)