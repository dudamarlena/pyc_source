# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/xcodeproj/xcodeproj.py
# Compiled at: 2019-02-23 14:43:19
# Size of source mod 2**32: 2588 bytes
import os
from .pbProj import pbProj
import Helpers.Logger as Logger

class xcodeproj(object):

    def __init__(self, xcodeproj_file_path):
        if os.path.exists(xcodeproj_file_path):
            if xcodeproj_file_path.endswith(('.xcodeproj', '.pbproj')):
                self.file_path = xcodeproj_file_path
                pbxproj_file_path = os.path.join(self.file_path, 'project.pbxproj')
                if os.path.exists(pbxproj_file_path):
                    self.project_file = pbProj.PBXProj(pbxproj_file_path)
                else:
                    Logger.write().error('Could not find the pbxproj file!')
            else:
                Logger.write().error('Not a Xcode project file!')
        else:
            Logger.write().error('Could not find the Xcode project file!')

    def projects(self):
        return self.project_file.projects()