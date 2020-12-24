import vkbottle
from distutils.core import setup

setup(
  name='vkbottletest',
  packages=['vkbottle'],
  version=vkbottle.__version__,
  license='MIT',
  description='New bot-creating repo with options control like in the famous framework flask!',
  author='Arseniy Timonik',
  author_email='timonik.bss@gmail.com',
  url='https://github.com/timoniq/vkbottle',
  long_description=open('vkbottle/README.rst', encoding='utf-8').read(),
  download_url='https://github.com/timoniq/vkbottle/archive/v' + vkbottle.__version__ + '.tar.gz',
  keywords=['vk', 'vkontakte', 'vk-api', 'vk-bot', 'vkbottle', 'vk-bottle'],
  install_requires=['requests>=2.2', 'six'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)