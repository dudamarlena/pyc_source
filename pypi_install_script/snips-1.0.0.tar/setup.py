from setuptools import setup, find_packages

setup(
    name="snips",
    version="1.0.0", # PEP 440
    packages=find_packages(),
    install_requires=[
        'click',
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'snips = snips.snips:cli'
        ]
    }
)