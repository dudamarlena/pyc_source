# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/fftool/main.py
# Compiled at: 2016-05-05 18:56:07
from outlawg import Outlawg
from fftool import PATH_PREFS_ROOT
from arg_parser import arg_parser
from firefox_download import download
from firefox_profile import create_mozprofile, clean_profiles
from firefox_run import launch_firefox
Log = Outlawg()

def main():
    Log.header('FF-TOOL: download, install & launch Firefox!', 'XL', '=')
    options = arg_parser()
    if options.app and not PATH_PREFS_ROOT:
        Log.header('ERROR')
        print 'Missing path to $PATH_PREFS_ROOT directory.'
        print 'Please set the `PATH_PREFS_ROOT` environment variable and ' + 'try again.'
        exit()
    if options.clean_profiles:
        clean_profiles()
        return
    download(options.channel)
    if options.install_only:
        return
    if not options.no_profile:
        profile_path = create_mozprofile(options.profile, application=options.app, test_type=options.test_type, env=options.env)
    if not options.no_launch:
        launch_firefox(profile_path, channel=options.channel)


if __name__ == '__main__':
    main()