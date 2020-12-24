from setuptools import setup
import os

n = "invisible_ui"
p = [n]

for f in os.listdir(n):
    if os.path.isdir(os.path.join(n, f)):
        p.append(n + "." + f)
        print("Adding %s to packages." % os.path.join(n, f))

setup(
    name=n,
    version="2.2",
    description="Accessible UI elements for pygame.",
    long_description=("This provides an accessible invisible user interface library for developers to be able to create UI environments for screenreaders. Note that there are "
                      "no graphics used, it is simply a meta concept using pygame and accessible_output2 to give the illusion that the screenreader is navigating through a "
                      " user interface. SAPI is used as the default screenreader for windows if a known screenreader is not loaded. Further testing needs to be done to "
                      "confirm compatibility on other platforms."),
    url="http://github.com/tbreitenfeldt/invisible_ui.git",
    author="TJ Breitenfeldt and Chris Norman",
    author_email="timothyjb310@gmail.com",
    license="GPL",
    packages=p,
    zip_safe=True,
    keywords=[
        "ui",
        "user interface",
        "pygame",
        "accessible",
        "a11y",
        "accessible_output",
        "spoken",
        "menu",
        "element"
    ],
    install_requires=[
        "pygame",
        "accessible_output2"
    ],
    python_requires=">=3"
)
