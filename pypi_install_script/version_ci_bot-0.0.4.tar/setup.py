import setuptools

with open('README.md', 'r') as f:
  long_description = f.read()

setuptools.setup(
  name='version_ci_bot',
  version='0.0.4',
  author='Nikolaos Georgiou',
  author_email='Nikolaos.Georgiou@gmail.com',
  license='MIT',
  description='A bot that runs during CI and helps with versioning',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/ngeor/version-ci-bot',
  packages=setuptools.find_packages(),
  entry_points={
    'console_scripts': ['version_ci_bot=version_ci_bot.main:main']
  }
)
