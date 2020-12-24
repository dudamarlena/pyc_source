from distutils.core import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name = "swowpy",
    packages = ["swowpy"],
    version = "0.4.1",
    description = "Simple wrapper for OpenWeatherMap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "Yorozuya3",
    author_email = "yorozuya3@protonmail.com",
    url = "https://gitlab.com/Yorozuya3/swowpy",
    keyword = ["weather","openweathermap","swowpy"],
    install_requires=['requests'],
)
