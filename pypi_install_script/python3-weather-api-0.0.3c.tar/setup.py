from distutils.core import setup

setup(name='python3-weather-api',
      version='0.0.3c',
      description='A Python wrapper for the Yahoo Weather XML RSS feed.',
      url='https://github.com/stevob21/weather-api',
      author='AnthonyBloomer, Stephen Boyd',
      keywords=['weather', 'api'],
      author_email='ant0@protonmail.ch, stevob212@gmail.com',
      license='MIT',
      packages=['weather', 'weather.models'],
      install_requires=[
          'requests',
      ],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          "Topic :: Software Development :: Libraries",
          'Programming Language :: Python :: 3.0'
      ],
      zip_safe=False)
