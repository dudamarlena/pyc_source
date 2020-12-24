import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='text2ml',
    version='3.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/marminino/text2ml',
    author='Alisson Lauffer',
    author_email='alissonvitortc@gmail.com',
    description='A module for Telegram Bot API that can format text + entities into formatted text',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
