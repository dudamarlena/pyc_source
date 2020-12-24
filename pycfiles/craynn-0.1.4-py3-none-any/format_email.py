# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/c24b/projets/crawtext_kiss/packages/format_email.py
# Compiled at: 2014-10-27 08:39:17


def createhtmlmail(html, text, subject, fromEmail):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones"""
    import MimeWriter, mimetools, cStringIO
    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)
    writer = MimeWriter.MimeWriter(out)
    writer.addheader('From', fromEmail)
    writer.addheader('Subject', subject)
    writer.addheader('MIME-Version', '1.0')
    writer.startmultipartbody('alternative')
    writer.flushheaders()
    subpart = writer.nextpart()
    subpart.addheader('Content-Transfer-Encoding', 'quoted-printable')
    pout = subpart.startbody('text/plain', [('charset', 'us-ascii')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()
    subpart = writer.nextpart()
    subpart.addheader('Content-Transfer-Encoding', 'quoted-printable')
    pout = subpart.startbody('text/html', [('charset', 'us-ascii')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg