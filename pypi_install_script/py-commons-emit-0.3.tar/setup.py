from setuptools import setup, find_packages

setup(
    name = "py-commons-emit",
    version = "0.3",
    keywords= ("event", "async", "redis", "publish", "subscribe", "emit", "on"),
    description = "light way for python to fire and consume events",
    license = "MIT Licence",
    author = "Aaron Yang",
    author_email = "aaron_yang@jieyu.ai",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any"
)
