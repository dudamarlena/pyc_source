from setuptools import setup

setup(
      name='rotencrpyption',
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
                       '''
      )
