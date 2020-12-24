from setuptools import setup
setup(name = "edbot",
    version = "5.2.0",
    description = "Edbot Python API module",
	long_description = "A Python API for the Edbot Software. Code your robots in Python!",
    url = "http://support.ed.bot",
    author = "Clive Haworth",
    author_email = "support@ed.bot",
    packages = [ "edbot" ],
    install_requires = [ "ws4py", "requests" ],
    zip_safe = False
)