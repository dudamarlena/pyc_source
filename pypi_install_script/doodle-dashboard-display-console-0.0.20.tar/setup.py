import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "sketchingdev", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about['__name__'],
    version=about['__version__'],
    description="Console display for Doodle-Dashboard.",
    url="https://github.com/SketchingDev/Doodle-Dashboard-Console-Display",
    license="MIT",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "click",
        "doodle-dashboard>=0.0.16",
        "Pillow>=5.0.0, <6.0.0"
    ],
    entry_points={
        "doodledashboard.custom.displays": [
            "console=sketchingdev.console:ConsoleDisplay"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.4"
    ],
    python_requires=">=3.4"
)
