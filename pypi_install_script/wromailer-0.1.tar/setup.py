from setuptools import setup, find_packages

setup(
    name="wromailer",
    version="0.1",
    packages=[
        "wromailer"
    ],
    install_requires=[
        "icalendar"
    ],
    entry_points={
        "console_scripts": [
            "wromailer = wromailer.remind:main_console"
        ]
    }
)