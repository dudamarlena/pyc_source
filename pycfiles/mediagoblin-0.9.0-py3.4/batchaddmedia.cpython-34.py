# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/gmg_commands/batchaddmedia.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 8037 bytes
from __future__ import print_function
import codecs, csv, os, requests, six
from six.moves.urllib.parse import urlparse
from mediagoblin.db.models import LocalUser
from mediagoblin.gmg_commands import util as commands_util
from mediagoblin.submit.lib import submit_media, get_upload_file_limits, FileUploadLimit, UserUploadLimit, UserPastUploadLimit
from mediagoblin.tools.metadata import compact_and_validate
from mediagoblin.tools.translate import pass_to_ugettext as _
from jsonschema.exceptions import ValidationError

def parser_setup(subparser):
    subparser.description = 'This command allows the administrator to upload many media files at once.'
    subparser.epilog = _('For more information about how to properly run this\nscript (and how to format the metadata csv file), read the MediaGoblin\ndocumentation page on command line uploading\n<http://docs.mediagoblin.org/siteadmin/commandline-upload.html>')
    subparser.add_argument('username', help=_('Name of user these media entries belong to'))
    subparser.add_argument('metadata_path', help=_('Path to the csv file containing metadata information.'))
    subparser.add_argument('--celery', action='store_true', help=_("Don't process eagerly, pass off to celery"))


def batchaddmedia(args):
    if not args.celery:
        os.environ['CELERY_ALWAYS_EAGER'] = 'true'
    app = commands_util.setup_app(args)
    files_uploaded, files_attempted = (0, 0)
    user = app.db.LocalUser.query.filter(LocalUser.username == args.username.lower()).first()
    if user is None:
        print(_("Sorry, no user by username '{username}' exists".format(username=args.username)))
        return
    upload_limit, max_file_size = get_upload_file_limits(user)
    temp_files = []
    if os.path.isfile(args.metadata_path):
        metadata_path = args.metadata_path
    else:
        error = _('File at {path} not found, use -h flag for help'.format(path=args.metadata_path))
        print(error)
        return
    abs_metadata_filename = os.path.abspath(metadata_path)
    abs_metadata_dir = os.path.dirname(abs_metadata_filename)
    upload_limit, max_file_size = get_upload_file_limits(user)

    def maybe_unicodeify(some_string):
        if some_string is None:
            return
        else:
            return six.text_type(some_string)

    with codecs.open(abs_metadata_filename, 'r', encoding='utf-8') as (all_metadata):
        contents = all_metadata.read()
        media_metadata = parse_csv_file(contents)
    for media_id, file_metadata in media_metadata.iteritems():
        files_attempted += 1
        json_ld_metadata = compact_and_validate({})
        original_location = file_metadata['location']
        title = file_metadata.get('title') or file_metadata.get('dc:title')
        description = file_metadata.get('description') or file_metadata.get('dc:description')
        license = file_metadata.get('license')
        try:
            json_ld_metadata = compact_and_validate(file_metadata)
        except ValidationError as exc:
            error = _("Error with media '{media_id}' value '{error_path}': {error_msg}\nMetadata was not uploaded.".format(media_id=media_id, error_path=exc.path[0], error_msg=exc.message))
            print(error)
            continue

        url = urlparse(original_location)
        filename = url.path.split()[(-1)]
        if url.scheme == 'http':
            res = requests.get(url.geturl(), stream=True)
            media_file = res.raw
        elif url.scheme == '':
            path = url.path
            if os.path.isabs(path):
                file_abs_path = os.path.abspath(path)
            else:
                file_path = os.path.join(abs_metadata_dir, path)
                file_abs_path = os.path.abspath(file_path)
            try:
                media_file = file(file_abs_path, 'r')
            except IOError:
                print(_('FAIL: Local file {filename} could not be accessed.\n{filename} will not be uploaded.'.format(filename=filename)))
                continue

        try:
            submit_media(mg_app=app, user=user, submitted_file=media_file, filename=filename, title=maybe_unicodeify(title), description=maybe_unicodeify(description), license=maybe_unicodeify(license), metadata=json_ld_metadata, tags_string='', upload_limit=upload_limit, max_file_size=max_file_size)
            print(_('Successfully submitted {filename}!\nBe sure to look at the Media Processing Panel on your website to be sure it\nuploaded successfully.'.format(filename=filename)))
            files_uploaded += 1
        except FileUploadLimit:
            print(_('FAIL: This file is larger than the upload limits for this site.'))
        except UserUploadLimit:
            print(_('FAIL: This file will put this user past their upload limits.'))
        except UserPastUploadLimit:
            print(_('FAIL: This user is already past their upload limits.'))

    print(_('{files_uploaded} out of {files_attempted} files successfully submitted'.format(files_uploaded=files_uploaded, files_attempted=files_attempted)))


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data), dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [six.text_type(cell, 'utf-8') for cell in row]


def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')


def parse_csv_file(file_contents):
    """
    The helper function which converts the csv file into a dictionary where each
    item's key is the provided value 'id' and each item's value is another
    dictionary.
    """
    list_of_contents = file_contents.split('\n')
    key, lines = list_of_contents[0].split(','), list_of_contents[1:]
    objects_dict = {}
    for index, line in enumerate(lines):
        if not line.isspace():
            if line == '':
                continue
            values = unicode_csv_reader([line]).next()
            line_dict = dict([(key[i], val) for i, val in enumerate(values)])
            media_id = line_dict.get('id') or index
            objects_dict[media_id] = line_dict

    return objects_dict