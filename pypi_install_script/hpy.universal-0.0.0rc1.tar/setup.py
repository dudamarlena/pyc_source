from setuptools import setup, Extension

setup(
    name="hpy.universal",
    packages = ['hpy.devel'],
    version='0.0.0-rc1',
    include_package_data=True,
    ext_modules = [
        Extension('hpy.universal',
                  ['hpy/universal/src/hpymodule.c',
                   'hpy/universal/src/handles.c',
                   'hpy/universal/src/api.c',
                  ],
                  include_dirs=['hpy/devel/include'],
        )]

)
