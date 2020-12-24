from setuptools import setup, find_packages

setup(
    name="aioffsend",
    version='0.0.1',
    description='a asyncio port for firefox send.',
    author='Chenwe-i-lin',
    author_email="Chenwe_i_lin@outlook.com",
    url="https://github.com/Chenwe-i-lin/aioffsend",
    packages=find_packages(include=("aioffsend", "aioffsend.*")),
    python_requires='>=3.7',
    keywords=["oicq qq qqbot", ],
    install_requires=[
        "aiohttp",
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent"
    ]
)