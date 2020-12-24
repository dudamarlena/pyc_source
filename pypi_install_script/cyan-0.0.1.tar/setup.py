import os
import sys
from setuptools import setup, find_packages

setup(
    name="cyan",
    version='0.0.1',
    description="Project Template",
    # long_description='nope',
    long_description_content_type="text/markdown",
    # url="https://gitlab.com/kabaretstudio/kabaret.subprocess_manager",
    author='Damien "dee" Coureau',
    author_email="dee@dee909.com",
    license="LGPLv3+",
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # "Development Status :: 4 - Beta",
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        # "Topic :: System :: Shells",
        # "Intended Audience :: Developers",
        # 'Intended Audience :: End Users/Desktop',
        # "Operating System :: Microsoft :: Windows :: Windows 10",
        # 'Programming Language :: Python :: 2.7',
        # "Programming Language :: Python :: 3.7",
        # "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    # keywords="",
    install_requires=[],
    # extras_require={"dev": ["twine", "flake8", "black",],},
    python_requires=">=3.7",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["*.css", "*.png", "*.svg", "*.gif"],},
)
