# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_submission.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 23528 bytes
SKIP_AUDIO = False
SKIP_VIDEO = False
try:
    import gi.repository.Gst, gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    Gst.init(None)
    from .media_tools import create_av
except ImportError:
    SKIP_AUDIO = True
    SKIP_VIDEO = True

try:
    import scikits.audiolab
except ImportError:
    SKIP_AUDIO = True

import six
if six.PY2:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
import os, pytest, webtest.forms, pkg_resources, six.moves.urllib.parse as urlparse
from mediagoblin.tests.tools import fixture_add_user, fixture_add_collection, get_app
from mediagoblin import mg_globals
from mediagoblin.db.models import MediaEntry, User, LocalUser, Activity
from mediagoblin.db.base import Session
from mediagoblin.tools import template
from mediagoblin.media_types.image import ImageMediaManager
from mediagoblin.media_types.pdf.processing import check_prerequisites as pdf_check_prerequisites
from .resources import GOOD_JPG, GOOD_PNG, EVIL_FILE, EVIL_JPG, EVIL_PNG, BIG_BLUE, GOOD_PDF, GPS_JPG, MED_PNG, BIG_PNG
GOOD_TAG_STRING = 'yin,yang'
BAD_TAG_STRING = six.text_type('rage,' + 'f' * 26 + 'u' * 26)
FORM_CONTEXT = [
 'mediagoblin/submit/start.html', 'submit_form']
REQUEST_CONTEXT = ['mediagoblin/user_pages/user.html', 'request']

@pytest.fixture()
def audio_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests', 'test_mgoblin_app_audio.ini'))


@pytest.fixture()
def video_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests', 'test_mgoblin_app_video.ini'))


@pytest.fixture()
def audio_video_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests', 'test_mgoblin_app_audio_video.ini'))


@pytest.fixture()
def pdf_plugin_app(request):
    return get_app(request, mgoblin_config=pkg_resources.resource_filename('mediagoblin.tests', 'test_mgoblin_app_pdf.ini'))


class BaseTestSubmission:

    @pytest.fixture(autouse=True)
    def setup(self, test_app):
        self.test_app = test_app
        fixture_add_user(privileges=['active', 'uploader', 'commenter'])
        self.login()

    def our_user(self):
        """
        Fetch the user we're submitting with.  Every .get() or .post()
        invalidates the session; this is a hacky workaround.
        """
        return LocalUser.query.filter(LocalUser.username == 'chris').first()

    def login(self):
        self.test_app.post('/auth/login/', {'username': 'chris', 
         'password': 'toast'})

    def logout(self):
        self.test_app.get('/auth/logout/')

    def do_post(self, data, *context_keys, **kwargs):
        url = kwargs.pop('url', '/submit/')
        do_follow = kwargs.pop('do_follow', False)
        template.clear_test_template_context()
        response = self.test_app.post(url, data, **kwargs)
        if do_follow:
            response.follow()
        context_data = template.TEMPLATE_TEST_CONTEXT
        for key in context_keys:
            context_data = context_data[key]

        return (
         response, context_data)

    def upload_data(self, filename):
        return {'upload_files': [('file', filename)]}

    def check_comments(self, request, media_id, count):
        gmr = request.db.GenericModelReference.query.filter_by(obj_pk=media_id, model_type=request.db.MediaEntry.__tablename__).first()
        if gmr is None and count <= 0:
            return
        comments = request.db.Comment.query.filter_by(target_id=gmr.id)
        assert count == comments.count()

    def check_url(self, response, path):
        assert urlparse.urlsplit(response.location)[2] == path

    def check_normal_upload(self, title, filename):
        response, context = self.do_post({'title': title}, do_follow=True, **self.upload_data(filename))
        self.check_url(response, '/u/{0}/'.format(self.our_user().username))
        assert 'mediagoblin/user_pages/user.html' in context
        url = '/u/{0}/m/{1}/'.format(self.our_user().username, title.lower().replace(' ', '-'))
        self.test_app.get(url)
        self.logout()
        self.test_app.get(url)

    def user_upload_limits(self, uploaded=None, upload_limit=None):
        our_user = self.our_user()
        if uploaded:
            our_user.uploaded = uploaded
        if upload_limit:
            our_user.upload_limit = upload_limit
        our_user.save()
        Session.expunge(our_user)


class TestSubmissionBasics(BaseTestSubmission):

    def test_missing_fields(self):
        response, form = self.do_post({}, *FORM_CONTEXT)
        assert form.file.errors == ['You must provide a file.']
        response, form = self.do_post({'title': 'test title'}, *FORM_CONTEXT)
        assert form.file.errors == ['You must provide a file.']

    def test_normal_jpg(self):
        assert self.our_user().uploaded == 0
        self.check_normal_upload('Normal upload 1', GOOD_JPG)
        file_size = os.stat(GOOD_JPG).st_size / 1048576.0
        file_size = float('{0:.2f}'.format(file_size))
        assert self.our_user().uploaded == file_size

    def test_public_id_populated(self):
        response, request = self.do_post({'title': 'Balanced Goblin'}, do_follow=True, *REQUEST_CONTEXT, **self.upload_data(GOOD_JPG))
        media = self.check_media(request, {'title': 'Balanced Goblin'}, 1)
        assert media.public_id != None

    def test_normal_png(self):
        self.check_normal_upload('Normal upload 2', GOOD_PNG)

    def test_default_upload_limits(self):
        self.user_upload_limits(uploaded=500)
        assert self.our_user().uploaded == 500
        response, context = self.do_post({'title': 'Normal upload 4'}, do_follow=True, **self.upload_data(GOOD_JPG))
        self.check_url(response, '/u/{0}/'.format(self.our_user().username))
        assert 'mediagoblin/user_pages/user.html' in context
        assert self.our_user().uploaded == 500

    def test_user_upload_limit(self):
        self.user_upload_limits(uploaded=25, upload_limit=25)
        assert self.our_user().uploaded == 25
        response, context = self.do_post({'title': 'Normal upload 5'}, do_follow=True, **self.upload_data(GOOD_JPG))
        self.check_url(response, '/u/{0}/'.format(self.our_user().username))
        assert 'mediagoblin/user_pages/user.html' in context
        assert self.our_user().uploaded == 25

    def test_user_under_limit(self):
        self.user_upload_limits(uploaded=499)
        assert self.our_user().uploaded == 499
        response, context = self.do_post({'title': 'Normal upload 6'}, do_follow=False, **self.upload_data(MED_PNG))
        form = context['mediagoblin/submit/start.html']['submit_form']
        assert form.file.errors == ['Sorry, uploading this file will put you over your upload limit.']
        assert self.our_user().uploaded == 499

    def test_big_file(self):
        response, context = self.do_post({'title': 'Normal upload 7'}, do_follow=False, **self.upload_data(BIG_PNG))
        form = context['mediagoblin/submit/start.html']['submit_form']
        assert form.file.errors == ['Sorry, the file size is too big.']

    def check_media(self, request, find_data, count=None):
        media = MediaEntry.query.filter_by(**find_data)
        if count is not None:
            assert media.count() == count
            if count == 0:
                return
        return media[0]

    def test_tags(self):
        response, request = self.do_post({'title': 'Balanced Goblin 2',  'tags': GOOD_TAG_STRING}, do_follow=True, *REQUEST_CONTEXT, **self.upload_data(GOOD_JPG))
        media = self.check_media(request, {'title': 'Balanced Goblin 2'}, 1)
        assert media.tags[0]['name'] == 'yin'
        assert media.tags[0]['slug'] == 'yin'
        assert media.tags[1]['name'] == 'yang'
        assert media.tags[1]['slug'] == 'yang'
        response, form = self.do_post({'title': 'Balanced Goblin 2',  'tags': BAD_TAG_STRING}, *FORM_CONTEXT, **self.upload_data(GOOD_JPG))
        assert form.tags.errors == [
         'Tags must be shorter than 50 characters.  Tags that are too long: ffffffffffffffffffffffffffuuuuuuuuuuuuuuuuuuuuuuuuuu']

    def test_delete(self):
        self.user_upload_limits(uploaded=50)
        response, request = self.do_post({'title': 'Balanced Goblin'}, do_follow=True, *REQUEST_CONTEXT, **self.upload_data(GOOD_JPG))
        media = self.check_media(request, {'title': 'Balanced Goblin'}, 1)
        media_id = media.id
        edit_url = request.urlgen('mediagoblin.edit.edit_media', user=self.our_user().username, media_id=media_id)
        self.test_app.get(edit_url)
        self.test_app.post(edit_url, {'title': 'Balanced Goblin',  'slug': 'Balanced=Goblin', 
         'tags': ''})
        media = self.check_media(request, {'title': 'Balanced Goblin'}, 1)
        assert media.slug == 'balanced-goblin'
        self.check_comments(request, media_id, 0)
        comment_url = request.urlgen('mediagoblin.user_pages.media_post_comment', user=self.our_user().username, media_id=media_id)
        response = self.do_post({'comment_content': 'i love this test'}, url=comment_url, do_follow=True)[0]
        self.check_comments(request, media_id, 1)
        delete_url = request.urlgen('mediagoblin.user_pages.media_confirm_delete', user=self.our_user().username, media_id=media_id)
        response = self.do_post({}, do_follow=True, url=delete_url)[0]
        media = self.check_media(request, {'title': 'Balanced Goblin'}, 1)
        media_id = media.id
        response, request = self.do_post({'confirm': 'y'}, *REQUEST_CONTEXT, do_follow=True, url=delete_url)
        self.check_media(request, {'id': media_id}, 0)
        self.check_comments(request, media_id, 0)
        assert self.our_user().uploaded == 50

    def test_evil_file(self):
        response, form = self.do_post({'title': 'Malicious Upload 1'}, *FORM_CONTEXT, **self.upload_data(EVIL_FILE))
        assert len(form.file.errors) == 1
        assert "Sorry, I don't support that file type :(" == str(form.file.errors[0])

    def test_get_media_manager(self):
        """Test if the get_media_manger function returns sensible things
        """
        response, request = self.do_post({'title': 'Balanced Goblin'}, do_follow=True, *REQUEST_CONTEXT, **self.upload_data(GOOD_JPG))
        media = self.check_media(request, {'title': 'Balanced Goblin'}, 1)
        assert media.media_type == 'mediagoblin.media_types.image'
        assert isinstance(media.media_manager, ImageMediaManager)
        assert media.media_manager.entry == media

    def test_sniffing(self):
        """
        Test sniffing mechanism to assert that regular uploads work as intended
        """
        template.clear_test_template_context()
        response = self.test_app.post('/submit/', {'title': 'UNIQUE_TITLE_PLS_DONT_CREATE_OTHER_MEDIA_WITH_THIS_TITLE'}, upload_files=[
         (
          'file', GOOD_JPG)])
        response.follow()
        context = template.TEMPLATE_TEST_CONTEXT['mediagoblin/user_pages/user.html']
        request = context['request']
        media = request.db.MediaEntry.query.filter_by(title='UNIQUE_TITLE_PLS_DONT_CREATE_OTHER_MEDIA_WITH_THIS_TITLE').first()
        assert media.media_type == 'mediagoblin.media_types.image'

    def check_false_image(self, title, filename):
        response, context = self.do_post({'title': title}, do_follow=True, **self.upload_data(filename))
        self.check_url(response, '/u/{0}/'.format(self.our_user().username))
        entry = mg_globals.database.MediaEntry.query.filter_by(title=title).first()
        assert entry.state == 'failed'
        assert entry.fail_error == 'mediagoblin.processing:BadMediaFail'

    def test_evil_jpg(self):
        self.check_false_image('Malicious Upload 2', EVIL_JPG)

    def test_evil_png(self):
        self.check_false_image('Malicious Upload 3', EVIL_PNG)

    def test_media_data(self):
        self.check_normal_upload('With GPS data', GPS_JPG)
        media = self.check_media(None, {'title': 'With GPS data'}, 1)
        assert media.get_location.position['latitude'] == 59.336666666666666

    def test_processing(self):
        public_store_dir = mg_globals.global_config['storage:publicstore']['base_dir']
        data = {'title': 'Big Blue'}
        response, request = self.do_post(data, do_follow=True, *REQUEST_CONTEXT, **self.upload_data(BIG_BLUE))
        media = self.check_media(request, data, 1)
        last_size = 1073741824
        for key, basename in (('original', 'bigblue.png'), ('medium', 'bigblue.medium.png'),
                              ('thumb', 'bigblue.thumbnail.png')):
            filename = os.path.join(public_store_dir, *media.media_files[key])
            assert filename.endswith('_' + basename)
            size = os.stat(filename).st_size
            assert last_size > size
            last_size = size

    def test_collection_selection(self):
        """Test the ability to choose a collection when submitting media
        """
        response = self.test_app.get('/submit/')
        assert 'collection' not in response.form.fields
        upload = webtest.forms.Upload(os.path.join('mediagoblin', 'static', 'images', 'media_thumbs', 'image.png'))
        response.form['file'] = upload
        no_collection_title = 'no collection'
        response.form['title'] = no_collection_title
        response.form.submit()
        assert MediaEntry.query.filter_by(actor=self.our_user().id).first().title == no_collection_title
        col = fixture_add_collection(user=self.our_user())
        user = fixture_add_user(username='different')
        fixture_add_collection(user=user, name='different')
        response = self.test_app.get('/submit/')
        form = response.form
        assert 'collection' in form.fields
        assert len(form['collection'].options) == 2
        assert form['collection'].options[1][2] == col.title
        form['file'] = upload
        title = 'new picture'
        form['title'] = title
        form['collection'] = form['collection'].options[1][0]
        form.submit()
        col = self.our_user().collections[0]
        assert col.collection_items[0].get_object().title == title
        assert Activity.query.order_by(Activity.id.desc()).first().content == '{0} added new picture to {1}'.format(self.our_user().username, col.title)
        form['file'] = webtest.forms.Upload(os.path.join('mediagoblin', 'static', 'images', 'media_thumbs', 'image.png'))
        title = 'no collection 2'
        form['title'] = title
        form['collection'] = form['collection'].options[0][0]
        form.submit()
        assert MediaEntry.query.filter_by(actor=self.our_user().id).count() == 3


class TestSubmissionVideo(BaseTestSubmission):

    @pytest.fixture(autouse=True)
    def setup(self, video_plugin_app):
        self.test_app = video_plugin_app
        fixture_add_user(privileges=['active', 'uploader', 'commenter'])
        self.login()

    @pytest.mark.skipif(SKIP_VIDEO, reason='Dependencies for video not met')
    def test_video(self, video_plugin_app):
        with create_av(make_video=True) as (path):
            self.check_normal_upload('Video', path)


class TestSubmissionAudio(BaseTestSubmission):

    @pytest.fixture(autouse=True)
    def setup(self, audio_plugin_app):
        self.test_app = audio_plugin_app
        fixture_add_user(privileges=['active', 'uploader', 'commenter'])
        self.login()

    @pytest.mark.skipif(SKIP_AUDIO, reason='Dependencies for audio not met')
    def test_audio(self, audio_plugin_app):
        with create_av(make_audio=True) as (path):
            self.check_normal_upload('Audio', path)


class TestSubmissionAudioVideo(BaseTestSubmission):

    @pytest.fixture(autouse=True)
    def setup(self, audio_video_plugin_app):
        self.test_app = audio_video_plugin_app
        fixture_add_user(privileges=['active', 'uploader', 'commenter'])
        self.login()

    @pytest.mark.skipif(SKIP_AUDIO or SKIP_VIDEO, reason='Dependencies for audio or video not met')
    def test_audio_and_video(self):
        with create_av(make_audio=True, make_video=True) as (path):
            self.check_normal_upload('Audio and Video', path)


class TestSubmissionPDF(BaseTestSubmission):

    @pytest.fixture(autouse=True)
    def setup(self, pdf_plugin_app):
        self.test_app = pdf_plugin_app
        fixture_add_user(privileges=['active', 'uploader', 'commenter'])
        self.login()

    @pytest.mark.skipif('not os.path.exists(GOOD_PDF) or not pdf_check_prerequisites()')
    def test_normal_pdf(self):
        response, context = self.do_post({'title': 'Normal upload 3 (pdf)'}, do_follow=True, **self.upload_data(GOOD_PDF))
        self.check_url(response, '/u/{0}/'.format(self.our_user().username))
        assert 'mediagoblin/user_pages/user.html' in context