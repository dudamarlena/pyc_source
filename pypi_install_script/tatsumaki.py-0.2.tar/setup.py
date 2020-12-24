try:
    from setuptools import setup
    import setuptools
except ImportError:
    from distutils.core import setup

setup(
    name='tatsumaki.py',
    version='0.2',
    install_requires=['aiohttp'],
    license='MIT License',
    packages=["tatsumaki"],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    description="An async python API Wrapper for the Tatsumaki API.",
    url="https://github.com/PumPum7/Tatsumaki.py/tree/master",
    author="Pum",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
