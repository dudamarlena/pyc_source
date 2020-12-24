# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/cli/commands.py
# Compiled at: 2019-04-24 05:47:57
# Size of source mod 2**32: 2923 bytes
import click, pymongo
from pymongo.errors import ConnectionFailure
from flask.cli import FlaskGroup, with_appcontext, current_app
from flask_mail import Message
from patientMatcher.server import create_app
from .add import add
from .remove import remove
from .update import update
cli = FlaskGroup(create_app=create_app)

@click.group()
def test():
    """Test server using CLI"""
    pass


@cli.command()
@with_appcontext
def name():
    """Returns the app name, for testing purposes, mostly"""
    app_name = current_app.name.split('.')[0]
    click.echo(app_name)
    return app_name


@cli.command()
@with_appcontext
@click.option('-recipient', type=(click.STRING), nargs=1, required=True, help='Email address to send the test email to')
def email(recipient):
    """Sends a test email using config settings"""
    click.echo(recipient)
    subj = 'Test email from patientMatcher'
    body = '\n        ***This is an automated message, please do not reply to this email.***<br><br>\n        If you receive this email it means that email settings are working fine and the\n        server will be able to send match notifications.<br>\n        A mail notification will be sent when:<br>\n        <ul>\n            <li>A patient is added to the database and the add request triggers a search\n            on external nodes producing at least one result (/patient/add endpoint).</li>\n\n            <li>An external search is actively performed on connected nodes and returns\n            at least one result (/match/external/<patient_id> endpoint).</li>\n\n            <li>The server is interrogated by an external node and returns at least one\n            result match (/match endpoint). In this case a match notification is sent to\n             each contact of the result matches.</li>\n\n            <li>An internal search is submitted to the server using a patient from the\n            database (/match endpoint) and this search returns at least one match.\n            In this case contact users of all patients involved will be notified\n            (contact from query patient and contacts from the result patients).</li>\n        </ul>\n        <br>\n        You can stop server notification any time by commenting the MAIL_SERVER parameter in\n        config file and rebooting the server.\n        <br><br>\n        Kind regards,<br>\n        The PatientMatcher team\n    '
    kwargs = dict(subject=subj, html=body, sender=(current_app.config.get('MAIL_USERNAME')), recipients=[recipient])
    message = Message(**kwargs)
    try:
        current_app.mail.send(message)
        click.echo('Mail correctly sent. Check your inbox!')
    except Exception as err:
        click.echo('An error occurred while sending test email: "{}"'.format(err))


test.add_command(name)
test.add_command(email)
cli.add_command(test)
cli.add_command(add)
cli.add_command(update)
cli.add_command(remove)