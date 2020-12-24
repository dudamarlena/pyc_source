try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def markdown_description(file_name):
    desc = pypandoc.convert(file_name, 'rst', format='md')
    return desc


try:
    import pypandoc
    long_description = markdown_description('README.md')
except ImportError:
    long_description = 'See README.md'

config = {
    'name': 'rabeye',
    'description': 'Simple RMQ CLI Monitor',
    'version': '0.0.9',
    'long_description': long_description,
    'license': "MIT",
    'author': 'Steve Hutchins',
    'author_email': 'hutchinsteve@gmail.com',
    'url': 'https://github.com/steveYeah/RabEye',
    'download_url': 'https://github.com/steveYeah/RabEye/archive/v0.0.9.tar.gz',
    'keywords': ['rabbitmq', 'rabbit', 'amqp', 'monitor', 'notifier', 'notifications'],
    'scripts': ['rabeye'],
    'data_files': [('/etc', ['rabeye-config.yaml'])],
    'install_requires': [
        'PyYAML',
        'pika',
    ],
}

setup(**config)
