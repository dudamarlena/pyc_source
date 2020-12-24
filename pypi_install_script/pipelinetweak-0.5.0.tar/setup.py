from setuptools import setup


def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pipelinetweak',
      version='0.5.0',
      description='additional wrapper classes for the sklearn API',
      # long_description=read('README.md'),
      # long_description_content_type='text/markdown',
      url='http://github.com/ulf1/sklearn-pipelinetweak',
      author='Ulf Hamster',
      author_email='554c46@gmail.com',
      license='MIT',
      packages=['pipelinetweak'],
      install_requires=[
          'setuptools>=40.0.0',
          'scikit-learn>=0.21.*',
          'numpy>=1.17.*',
          'lagmat>=0.3.*'],
      python_requires='>=3.6',
      zip_safe=False)
