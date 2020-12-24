from setuptools import setup

setup(
    name = 'yaargh-dummy-argh',
    description = 'Dummy argh module that proxies yaargh',
    version = '0.0.2',
    py_modules = ['argh'],
    install_requires = ['yaargh'],
    author = 'Mike Lang',
    author_email = 'mikelang3000+yaargh@gmail.com',
)
