# download the latest version of package from github, and run setup.py from that package
import os, sys, subprocess
try:        from urllib.request import urlretrieve  # Python 3
except ImportError: from urllib import urlretrieve  # Python 2

# print messages directly to terminal, bypassing pip's pipe
def say(text):
    sys.stdout.write(text)
    sys.stdout.flush()
    if not sys.stdout.isatty():
        # output was redirected, but we still try to send the message to the terminal
        try:
            with open('/dev/tty','w') as out:
                out.write(text)
                out.flush()
        except:
            # /dev/tty may not exist or may not be writable!
            pass

say('Running '+__file__+'\nDownloading the latest version of package from github\n')
try:
    filename = 'agama.zip'
    dirname  = 'Agama-master'
    urlretrieve('https://github.com/GalacticDynamics-Oxford/Agama/archive/master.zip', filename)
    # unpack/move files to the current directory, overwriting this setup.py by the one from the package
    subprocess.call('unzip '+filename+' >/dev/null', shell=True)
    subprocess.call('mv -f '+dirname+'/* .', shell=True)
    if os.path.getsize(__file__) < 10000:  # the new setup.py should be large enough, or else something must have gone wrong
        raise RuntimeError('Failed to download the package from github')
    # now transfer control to setup.py from the package
    exit(subprocess.call(sys.executable + ' ' + ' '.join([x if x!='-c' else __file__ for x in sys.argv]), shell=True))
except Exception as ex:
    say('Exception: '+str(ex)+'\n')
    exit(1)
