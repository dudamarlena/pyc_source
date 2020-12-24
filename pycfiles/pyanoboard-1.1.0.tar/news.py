# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyano/news.py
# Compiled at: 2010-11-11 20:44:57
from validate import *
from config import conf, POST
from interface import MixInterface
from stats import bad_mail2news, format_bad_mail2news, mail2news_pref_sort
from mix import send_news

class NewsInterface(MixInterface):
    form_html = '\n    <form action="PYANO_URI" method="post" >\n    <table id="mixtable">\n      <tr id="newsgroup">\n        <td><strong>*Newsgroup(s):</strong></td>\n        <td><input class="line" name="newsgroups" value="" /></td>\n      </tr>\n      <tr id="from">\n        <td><strong>From:</strong></td>\n        <td><input class="line" name="from" value="" /></td>\n      </tr>\n      <tr id="subject">\n        <td><strong>*Subject:</strong></td>\n        <td><input class="line" name="subject" value="" /></td>\n      </tr>\n      <tr>\n        <td><strong>References:</strong></td>\n        <td><input class="line" name="references" value="" /></td>\n      </tr>\n      <tr id="mail2news">\n        <td><strong>Mail2News:</strong></td>PYANO_MAIL2NEWS\n      </tr>\n      <tr id="hashcash">\n        <td><strong>Hashcash:</strong></td>\n        <td><input class="line" name="hashcash" value="" /></td>\n      </tr>\n      <tr id="noarchive">\n        <td><strong>X-No-Archive:</strong></td>\n        <td><input type="checkbox" name="archive" checked="checked" />\n        (checked means Google will not archive this post)\n        </td>\n      </tr>PYANO_CHAIN\n      <tr id="copies">\n         <td><strong>Copies:</strong></td>\n         <td>\n           PYANO_COPIES\n         </td>\n      </tr>\n      <tr id="message">\n        <td><strong>*Message:</strong></td>\n        <td><textarea name="message" rows="30" cols="70" ></textarea></td>\n      </tr>\n      <tr id="buttons">\n        <td></td>\n        <td><input type="submit" value="Send" /><input type="reset" value="Reset" /></td>\n      </tr>\n    </table>\n    </form>\n'

    def validate(self):
        groups = str(self.fs['newsgroups']).replace(' ', '')
        val_newsgroups(groups)
        orig = str(self.fs['from'])
        if orig:
            val_email(orig)
        refs = str(self.fs['references'])
        if refs:
            val_references(refs)
        mail2news_custom = self.fs['mail2news_custom']
        if mail2news_custom:
            val_mail2news(mail2news_custom)
            mail2news = mail2news_custom
        else:
            mail2news = str(self.fs['mail2news'])
            if mail2news != POST:
                val_mail2news(mail2news)
        hashcash = str(self.fs['hashcash']).strip()
        if hashcash:
            val_hashcash(hashcash)
        try:
            checked = str(self.fs['archive'])
            no_archive = True
        except KeyError:
            no_archive = False

        subj = str(self.fs['subject'])
        if not subj:
            raise InputError('Subject required.')
        chain = parse_chain(self.fs, m2n=mail2news)
        n_copies = int(self.fs['copies'])
        val_n_copies(n_copies)
        msg = str(self.fs['message'])
        if not msg:
            raise InputError('Refusing to send empty message.')
        return (groups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg)

    def html(self):
        return conf.news_html

    def form(self):
        mail2news = '\n'
        mail2news += '        <td>\n'
        mail2news += '          <select name="mail2news" >\n'
        if bad_mail2news:
            gateways = mail2news_pref_sort()
            for gateway in gateways:
                mail2news += '            <option value="' + gateway + '">' + format_bad_mail2news(gateway).replace(' ', '&nbsp;') + '</option>\n'

        for gateway in conf.mail2news:
            mail2news += '            <option value="' + gateway + '">' + gateway + '</option>\n'

        mail2news += '          </select><br/>\n'
        mail2news += '          Or custom: <input name="mail2news_custom" value="" />\n'
        mail2news += '        </td>\n'
        out = NewsInterface.form_html.replace('PYANO_MAIL2NEWS', mail2news)
        return conf.news_form_html.replace('<!--FORM-->', out)

    def process(self):
        (newsgroups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg) = self.validate()
        send_news(newsgroups, orig, subj, refs, mail2news, hashcash, no_archive, chain, n_copies, msg)
        msg = 'Successfully sent message to ' + newsgroups + ' using '
        if chain:
            msg += 'remailer chain ' + (',').join(chain)
        else:
            msg += 'a random remailer chain'
        if mail2news != POST:
            msg += ' with mail2news gateway ' + mail2news + '.'
        else:
            msg += '.'
        return msg


def handler(req):
    return NewsInterface()(req)