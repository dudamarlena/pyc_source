from setuptools import setup

setup(
    name = 'soakubot',
    version = '1.0.7',
    packages = ['bbcdom', 'soakubot'],
    install_requires=["requests", "lxml"],
    url = 'https://github.com/Soaku/OM-Bot',
    license = '(see repo)',
    author = 'Soaku',
    author_email = '',
    description = 'A bot for overmobile\'s games. Focused on mrush.pl.'
)
