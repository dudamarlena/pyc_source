# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/main_damreport.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 5813 bytes
__doc__ = '\nCreated on 19 Feb 2014\n\n@author: "Colin Manning"\n'
import sys, getopt, os, requests, json, smtplib, traceback
from email.mime.text import MIMEText
from email.header import Header
import utils
COMMASPACE = ', '
mail_server = None
mailer = None
mail_signature_logo = None
company_web_address = None

def get_email_dam_body(dam_report):
    return '<h3>Report for DAM Catalog</h3><hr /> <div> <table> <tr><td>Connection Name:</td><td>%s</td></tr> <tr><td>Catalog Name:</td><td>%s</td></tr> <tr><td>Files:</td><td>%i</td></tr> </table></div>' % (
     dam_report['connection_name'], dam_report['database_name'], dam_report['record_count'])


def get_email_summary_body(dam_reports):
    result = '<div><h3>Point Dam Usage Report</h3> <table> <tr><td style="font-weight:bold;border-bottom-style:solid;border-bottom-weight:thin;">Catalog</td><td style="font-weight:bold;border-bottom-style:solid;border-bottom-weight:thin;">File Count</td><tr>'
    total = 0
    for dam_report in dam_reports:
        dam_total = -1
        if 'record_count' in dam_report:
            dam_total = dam_report['record_count']
        else:
            print(' problem with dam report for %s' % dam_report['title'])
        total += dam_total
        result += '<tr><td style="font-weight:bold;">%s</td><td style="text-align:right;">%i</td><tr>' % (
         dam_report['title'], dam_total)
        for category in dam_report['categories']:
            category_report = dam_report['categories'][category]
            category_total = -1
            if 'record_count' in category_report:
                category_total = category_report['record_count']
            else:
                print(' problem with category report for %s' % category_report['title'])
            result += '<tr><td>- %s (%i)</td><td style="text-align:right;"></td><tr>' % (
             category, category_total)

    result += '</table></div><hr />'
    result += '<h3>Total: %i</h3><br />' % total
    return result


def setup_mailer(mail_server):
    global mail_signature_logo
    global mailer
    mail_signature_logo = mail_server['signature_logo']
    mailer = smtplib.SMTP(mail_server['host'], mail_server['port'])
    try:
        mailer.login(mail_server['default_login'], mail_server['default_password'])
    except:
        print('Failed to login to mail server')


def send_html_mail(receivers, subject, message):
    global mail_server
    try:
        send_message = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
        send_message['Subject'] = Header(subject, 'utf-8')
        send_message['From'] = mail_server['default_login']
        send_message['To'] = COMMASPACE.join(receivers)
        try:
            mailer.sendmail(mail_server['default_login'], receivers, send_message.as_string())
        except:
            setup_mailer(mail_server)
            mailer.sendmail(mail_server['default_login'], receivers, send_message.as_string())

    except:
        print('problem sending html email')
        traceback.print_exc()


def emailDamReport(dam_title, email_list, dam_report):
    global company_web_address
    subject = 'Point DAM Report for: ' + dam_title
    message = get_email_dam_body(dam_report)
    message += utils.get_email_company_footer(mail_signature_logo, company_web_address)
    send_html_mail(email_list, subject, message)


def emailSummaryReport(email_list, dam_reports):
    subject = 'Point DAM Usage Report'
    message = get_email_summary_body(dam_reports)
    message += utils.get_email_company_footer(mail_signature_logo, company_web_address)
    send_html_mail(email_list, subject, message)


def main():
    global company_web_address
    global mail_server
    configFile = None
    configData = None
    damReports = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c', ['configfile='])
    except getopt.GetoptError:
        print('Problem getting options')
        sys.exit(2)

    configFile = args[0]
    if configFile is not None and os.path.exists(configFile):
        with open(configFile) as (f):
            configData = json.load(f)
            f.close()
        mail_server = configData['mail_server']
        company_web_address = configData['company_web_address']
        setup_mailer(mail_server)
    else:
        print('Please specify a valid configuration file')
    for dam in configData['dams']:
        requestUrl = dam['baseurl'] + '/admin/' + dam['connection'] + '/catalogreport'
        disResponse = requests.get(requestUrl)
        report = disResponse.json()
        report['title'] = dam['title']
        report['categories'] = {}
        if 'categories' in dam:
            dam_total = 0
            for category in dam['categories']:
                requestUrl = dam['baseurl'] + '/admin/' + dam['connection'] + '/categoryreport'
                requestUrl += '?path=' + category['path']
                disResponse = requests.get(requestUrl)
                category_report = disResponse.json()
                dam_total += category_report['record_count']
                report['categories'][category['title']] = category_report

            report['record_count'] = dam_total
        damReports.append(report)

    emailSummaryReport(configData['email_list'], damReports)
    return


if __name__ == '__main__':
    main()