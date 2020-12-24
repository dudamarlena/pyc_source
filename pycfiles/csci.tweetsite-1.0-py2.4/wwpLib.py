# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/csci/tweetsite/browser/lib/wwpLib.py
# Compiled at: 2009-11-18 10:07:54
import urllib, datetime, time, random, unicodedata
from string import maketrans
from email.Header import make_header
from email.MIMEMessage import Message
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def nametoid(text):
    """change a name into an id"""
    try:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    except:
        pass

    illegal = '.,!"£$%^&*()_+=[]{}@#~?/><|\'¬`;:'
    for ill in illegal:
        text = text.replace(ill, '')

    text = text.replace('<br>', '')
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace(' ', '-')
    return text


def publishNews(context, title, description, text):
    """publishes a news item to the site repository"""
    _newsSubDir = 'news'
    today = datetime.date.today()
    news_id = str(title) + '-' + str(today)
    news_id += '-' + str(random.random() * 100)[:2]
    news_id = news_id.replace(' ', '-')
    news_id = _removeSymb(news_id)
    news_id = news_id.lower()
    root_app = context.restrictedTraverse(_newsSubDir)
    news_item = root_app.invokeFactory(type_name='News Item', id=news_id, title=title, description=description, text=text)
    root_app.reindexObject()
    root_app = context.restrictedTraverse('news/' + news_id)
    urltool = getToolByName(context, 'portal_url')
    workflow = getToolByName(context, 'portal_workflow')
    review_state = workflow.getInfoFor(root_app, 'review_state')
    if review_state != 'published':
        error = workflow.doActionFor(root_app, 'publish', comment='publised programmatically')
    root_app.reindexObject()


def postToTwitter(uname, passwd, text):
    """sends a post to twitter under specified username"""
    errors = ''
    try:
        api = twitter.Api(username=uname, password=passwd)
    except:
        errors += 'Twitter login fail'
        return errors

    try:
        statuses = api.PostUpdate(status=text[:140], in_reply_to_status_id=None)
    except:
        errors += 'Failed at posting'
        return errors

    return


def get_short(server='', action='get_or_create_hash', hmac='', email='', url='', short_name='anything', is_public='true'):
    request_url = google_short.make_request_uri(server, action, hmac, user=email, url=url, shortcut=short_name, is_public=str(is_public).lower())
    response = urllib.urlopen(request_url)
    res = response.read()
    res = res.replace('true', 'True')
    res_dict = eval(res)
    end_url = 'http://' + str(server) + '/' + str(res_dict['shortcut'])
    return end_url


def sendEmail(context, mTo, mFrom, mSubj, message, message_b):
    e_subject = mSubj
    e_from = mFrom
    e_to = mTo
    body_html = message
    body_plain = message_b
    mime_msg = MIMEMultipart('related')
    mime_msg['Subject'] = e_subject
    mime_msg['From'] = e_from
    mime_msg['To'] = e_to
    mime_msg.preamble = 'This is a multi-part message in MIME format.'
    msgAlternative = MIMEMultipart('alternative')
    mime_msg.attach(msgAlternative)
    if message_b != '':
        msg_txt = MIMEText(body_plain, _charset='iso-8859-1')
        msgAlternative.attach(msg_txt)
    if message != '':
        msg_txt = MIMEText(body_html, _subtype='html', _charset='iso-8859-1')
        msgAlternative.attach(msg_txt)
    context.MailHost.send(mime_msg.as_string())