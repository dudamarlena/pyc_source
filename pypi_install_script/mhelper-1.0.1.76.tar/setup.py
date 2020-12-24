from distutils.core import setup


def readme():
    try:
        import os
        readme_fn = os.path.join( os.path.dirname( __file__ ), "readme.rst" )
        with open( readme_fn ) as f:
            return f.read()
    except Exception as ex:
        return "Failed to read readme.rst due to an error: {}".format( ex )


setup( name = "mhelper",
       url = "https://bitbucket.org/mjr129/mhelper",
       version = "1.0.1.76",
       description = "Includes a collection of utility functions.",
       long_description = readme(),
       author = "Martin Rusilowicz",
       license = "https://www.gnu.org/licenses/agpl-3.0.html",
       python_requires = ">=3.7",
       include_package_data = True,

       packages = ["mhelper",
                   "mhelper.mannotation",
                   "mhelper_qt",
                   "mhelper_qt.designer",
                   "mhelper._unittests"
                   ],


       extras_require = { 'everything': ["jsonpickle",
                                         "PyQt5",
                                         "mistune",
                                         ],
                          'deprecated': ["py-flags"]
                          }
       )
