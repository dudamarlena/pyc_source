from setuptools import setup

__project__ = "keniProject2"
__version__ = "0.0.1"
__description__ = "a Python module to motivate you"
__packages__ = ["keniProject2"]
__author__ = "kenny388"
__author_email__ = "kenny388@hotmail.com"
__classifiers__ = [
	"Development Status :: 1 - Planning",
	"Natural Language :: Arabic",
	"Operating System :: Other OS",
]
__requires__ = ["guizero"]


setup(
	name = __project__,
	version = __version__,
	description = __description__,
	packages = __packages__,
	author = __author__,
	author_email = __author_email__,
	classifiers = __classifiers__,
	requires = __requires__,
)
