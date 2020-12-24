from setuptools import setup, find_packages

setup(
    name='test-rss-par',
    version='2.0.0',
    packages=find_packages(),
    author='Vadim Rashkevich',
    author_email='vadimrashkevich@yandex.ru',
    url='https://github.com/Solborm',
    python_requires='>=3.6',
    install_requires=['feedparser'],
)
