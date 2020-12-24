from setuptools import setup

setup(
  name = 'my-resume-generator',
  packages = ['my_resume_generator'],
  version = '0.1.1',
  description = 'A resume generator from a markdown file',
  author = 'Bruno Schmidt Mello',
  author_email = 'bruunoxp2@gmail.com',
  license='MIT',
  install_requires=[
    'markdown2==2.3.4', 'xhtml2pdf==0.2b1'
  ],
  url = 'https://github.com/bruno-schmidt/my-resume-generator',
  classifiers = [],
  entry_points={
      'console_scripts': [
          'my-resume-generator = my_resume_generator.my_resume_generator:run',
      ]
  },
)