# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/release/googlecode_upload.py
# Compiled at: 2008-12-17 17:49:00
__doc__ = 'Google Code file uploader script.\n'
__author__ = 'danderson@google.com (David Anderson)'
import httplib, os.path, optparse, getpass, base64, sys
saved_user_name = None
saved_password = None

def get_svn_config_dir():
    """Return user's Subversion configuration directory."""
    try:
        from win32com.shell.shell import SHGetFolderPath
        import win32com.shell.shellcon
    except ImportError:
        return os.path.expanduser('~/.subversion')

    return os.path.join(SHGetFolderPath(0, win32com.shell.shellcon.CSIDL_APPDATA, 0, 0).encode('utf-8'), 'Subversion')


def get_svn_auth(project_name, config_dir):
    """Return (username, password) for project_name in config_dir."""
    result = (None, None)
    try:
        from svn.core import SVN_AUTH_CRED_SIMPLE, svn_config_read_auth_data
        from svn.core import SubversionException
    except ImportError:
        return result

    realm = '<https://%s.googlecode.com:443> Google Code Subversion Repository' % project_name
    try:
        auth = svn_config_read_auth_data(SVN_AUTH_CRED_SIMPLE, realm, config_dir)
    except SubversionException:
        auth = None

    if auth is not None:
        try:
            result = (
             auth['username'], auth['password'])
        except KeyError:
            pass

    return result


def upload(file, project_name, user_name, password, summary, labels=None):
    """Upload a file to a Google Code project's file server.

  Args:
    file: The local path to the file.
    project_name: The name of your project on Google Code.
    user_name: Your Google account name.
    password: The googlecode.com password for your account.
              Note that this is NOT your global Google Account password!
    summary: A small description for the file.
    labels: an optional list of label strings with which to tag the file.

  Returns: a tuple:
    http_status: 201 if the upload succeeded, something else if an
                 error occured.
    http_reason: The human-readable string associated with http_status
    file_url: If the upload succeeded, the URL of the file on Google
              Code, None otherwise.
  """
    if user_name.endswith('@gmail.com'):
        user_name = user_name[:user_name.index('@gmail.com')]
    form_fields = [('summary', summary)]
    if labels is not None:
        form_fields.extend([ ('label', l.strip()) for l in labels ])
    (content_type, body) = encode_upload_request(form_fields, file)
    upload_host = '%s.googlecode.com' % project_name
    upload_uri = '/files'
    auth_token = base64.b64encode('%s:%s' % (user_name, password))
    headers = {'Authorization': 'Basic %s' % auth_token, 
       'User-Agent': 'Googlecode.com uploader v0.9.4', 
       'Content-Type': content_type}
    server = httplib.HTTPSConnection(upload_host)
    server.request('POST', upload_uri, body, headers)
    resp = server.getresponse()
    server.close()
    if resp.status == 201:
        location = resp.getheader('Location', None)
    else:
        location = None
    return (resp.status, resp.reason, location)


def encode_upload_request(fields, file_path):
    """Encode the given fields and file into a multipart form body.

  fields is a sequence of (name, value) pairs. file is the path of
  the file to upload. The file will be uploaded to Google Code with
  the same file name.

  Returns: (content_type, body) ready for httplib.HTTP instance
  """
    BOUNDARY = '----------Googlecode_boundary_reindeer_flotilla'
    CRLF = '\r\n'
    body = []
    for (key, value) in fields:
        body.extend([
         '--' + BOUNDARY,
         'Content-Disposition: form-data; name="%s"' % key,
         '',
         value])

    file_name = os.path.basename(file_path)
    f = open(file_path, 'rb')
    file_content = f.read()
    f.close()
    body.extend([
     '--' + BOUNDARY,
     'Content-Disposition: form-data; name="filename"; filename="%s"' % file_name,
     'Content-Type: application/octet-stream',
     '',
     file_content])
    body.extend(['--' + BOUNDARY + '--', ''])
    return (
     'multipart/form-data; boundary=%s' % BOUNDARY, CRLF.join(body))


def upload_find_auth(file_path, project_name, summary, labels=None, config_dir=None, user_name=None, tries=3):
    """Find credentials and upload a file to a Google Code project's file server.

  file_path, project_name, summary, and labels are passed as-is to upload.

  If config_dir is None, try get_svn_config_dir(); if it is 'none', skip
  trying the Subversion configuration entirely.  If user_name is not None, use
  it for the first attempt; prompt for subsequent attempts.

  Args:
    file_path: The local path to the file.
    project_name: The name of your project on Google Code.
    summary: A small description for the file.
    labels: an optional list of label strings with which to tag the file.
    config_dir: Path to Subversion configuration directory, 'none', or None.
    user_name: Your Google account name.
    tries: How many attempts to make.
  """
    global saved_password
    global saved_user_name
    if config_dir != 'none':
        if config_dir is None:
            config_dir = get_svn_config_dir()
        (svn_username, password) = get_svn_auth(project_name, config_dir)
        if user_name is None:
            user_name = svn_username
    else:
        password = None
    if saved_user_name is not None:
        user_name = saved_user_name
    if saved_password is not None:
        password = saved_password
    while tries > 0:
        if user_name is None:
            sys.stdout.write('Please enter your googlecode.com username: ')
            sys.stdout.flush()
            user_name = sys.stdin.readline().rstrip()
        if password is None:
            print 'Please enter your googlecode.com password.'
            print '** Note that this is NOT your Gmail account password! **'
            print 'It is the password you use to access Subversion repositories,'
            print 'and can be found here: http://code.google.com/hosting/settings'
            password = getpass.getpass()
        (status, reason, url) = upload(file_path, project_name, user_name, password, summary, labels)
        if status in [httplib.FORBIDDEN, httplib.UNAUTHORIZED]:
            user_name = password = None
            tries = tries - 1
        else:
            break

    saved_user_name = user_name
    saved_password = password
    return (
     status, reason, url)


def main():
    parser = optparse.OptionParser(usage='googlecode-upload.py -s SUMMARY -p PROJECT [options] FILE')
    parser.add_option('--config-dir', dest='config_dir', metavar='DIR', help='read svn auth data from DIR ("none" means not to use svn auth data)')
    parser.add_option('-s', '--summary', dest='summary', help='Short description of the file')
    parser.add_option('-p', '--project', dest='project', help='Google Code project name')
    parser.add_option('-u', '--user', dest='user', help='Your Google Code username')
    parser.add_option('-l', '--labels', dest='labels', help='An optional list of labels to attach to the file')
    (options, args) = parser.parse_args()
    if not options.summary:
        parser.error('File summary is missing.')
    elif not options.project:
        parser.error('Project name is missing.')
    elif len(args) < 1:
        parser.error('File to upload not provided.')
    elif len(args) > 1:
        parser.error('Only one file may be specified.')
    file_path = args[0]
    if options.labels:
        labels = options.labels.split(',')
    else:
        labels = None
    (status, reason, url) = upload_find_auth(file_path, options.project, options.summary, labels, options.config_dir, options.user)
    if url:
        print 'The file was uploaded successfully.'
        print 'URL: %s' % url
        return 0
    else:
        print 'An error occurred. Your file was not uploaded.'
        print 'Google Code upload server said: %s (%s)' % (reason, status)
        return 1
    return


if __name__ == '__main__':
    sys.exit(main())