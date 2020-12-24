from setuptools import setup
from os import getcwd

__path__ = getcwd()

setup(
      name='RotEncrypt',
      version='0.0.0',
      description='Encrypt words with rot',
      long_description='''
                Examples:
                import rot
                a = rot.Rot("hello")
                a.rot(13)
                
                will produce the output
                uryy|
                
                To get the normal unrotated word:
                
                a.unrot()
                
                will produce the output:
                'hello'
                       ''',
    long_description_content_type='x-rst'
                       )
