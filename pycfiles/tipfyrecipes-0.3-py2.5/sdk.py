# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tipfyrecipes/gae/sdk.py
# Compiled at: 2011-08-05 19:07:14
import os
from tipfyrecipes.download import Recipe as DownloadRecipe

class InstallGAE(DownloadRecipe):
    """
        Downloads and installs the App Engine SDK in the buildout directory.

        Options
        ~~~~~~~

        :url: URL to the App Engine SDK file.
        :destination: Destination of the extracted SDK. Default is the parts directory.
        :clear-destination: If `true`, deletes the destination dir before
                extracting the download. Default is `true`.

        Example
        ~~~~~~~

        ::

          [gae_sdk]
          recipe = appfy.recipe.gae:sdk
          url = http://googleappengine.googlecode.com/files/google_appengine_1.4.2.zip
          destination = ${buildout:parts-directory}
          hash-name = false
          clear-destination = true
        """

    def __init__(self, buildout, name, options):
        parts_dir = os.path.abspath(buildout['buildout']['parts-directory'])
        options.setdefault('destination', parts_dir)
        options.setdefault('clear-destination', 'true')
        super(InstallGAE, self).__init__(buildout, name, options)