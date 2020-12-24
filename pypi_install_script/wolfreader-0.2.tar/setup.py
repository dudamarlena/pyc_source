from setuptools import setup, find_packages

setup(
    name="wolfreader",
    version="0.2",
    description="A Screen Reader",
    author="midnio",
    maintainer="BTaskaya",
    packages=["wolf"],
    entry_points={
        "console_scripts": [
            "wolf=wolf.wolf:main"
        ]
    },
)
