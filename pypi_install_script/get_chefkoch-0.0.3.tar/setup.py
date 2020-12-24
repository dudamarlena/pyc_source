from setuptools import setup
__project__ = "get_chefkoch"
__version__ = "0.0.3"
__description__ = "A Python program with which you can get data from Chefkoch."
__packages__ = ["get_chefkoch"]
__keywords__ = ["Chefkoch","python"]
__requires__ = ["requests","feedparser","bs4","json","lxml"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    keywords = __keywords__,
    requires = __requires__,
)
