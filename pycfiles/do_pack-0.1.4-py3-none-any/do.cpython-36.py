# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\do.py
# Compiled at: 2018-03-05 09:17:00
# Size of source mod 2**32: 5410 bytes
"""
A simple and quick command line tool to create python packages.
"""
import do.template_config, do.skeleton, do.licenses, do.assist, do.config, click, sys, os

@click.group()
def main():
    """
    A simple and quick command line tool to create python packages.
    """
    pass


@main.command()
@click.option('--template', '-t', help='Lets you choose a Template.')
@click.argument('project-name')
def create(project_name, template):
    """
    creates a default python structure for your package or project.
    """
    notice = '\ndo will create your {} Project Structure.'.format(project_name)
    notice_t = '\ndo will create {} project using {} file Template.'.format(project_name, template)
    done = '{} was created on {}'
    if template:
        click.echo(notice_t)
        if click.confirm('Do you want to continue?'):
            do.skeleton.make_skeleton(project_name, template)
            click.echo(done.format(project_name, os.getcwd()))
    else:
        click.echo(notice)
    if click.confirm('Do you want to continue?'):
        do.skeleton.make_skeleton(project_name)
        click.echo(done.format(project_name, os.getcwd()))


@main.command()
def assistant():
    """
    A step by step assistant.
    """
    msg_notice = '>> do will now start the assistant. Do you want to continue?'
    msg_lice_ref = '(more detailed info in https://choosealicense.com):\n'
    msg_choose_lice = '\nEnter the number of the license to choose one'
    clear()
    if click.confirm(msg_notice):
        config_field = do.config.show_common
        default_author = config_field('default_author')
        default_mail = config_field('default_mail')
        project_name = click.prompt('\nproject name')
        setup_version = click.prompt('version', default='0.1.0dev')
        setup_description = click.prompt('description')
        setup_author = click.prompt('author', default=default_author)
        setup_author_email = click.prompt('author_email', default=default_mail)
        setup_url = click.prompt('url')
        click.echo('\n>> Select one of the following LICENSES ' + msg_lice_ref)
        do.licenses.show()
        lice_num = click.prompt(msg_choose_lice)
        chosen_licence = lice(lice_num, setup_author, project_name)
        setup = do.template_config.setup_template(project_name, setup_version, setup_description, setup_author, setup_author_email, setup_url)
        authors = do.template_config.authors_template(project_name, setup_author, setup_author_email)
        gitignore = do.template_config.gitignore_template()
        do.assist.make_skeleton(project_name, authors, chosen_licence, setup, gitignore)
        click.echo('\n>> {} was created on {}'.format(project_name, os.getcwd()))


@main.command()
def config():
    """
    A simple configuration for common fields (author_name
    and author_email).

    If executed twice, it will overwrite the previous one.
    """
    config_field = do.config.show_common
    default_author = config_field('default_author')
    default_mail = config_field('default_mail')
    msg_welcome = '\nWelcome to the configuration for common fields.'
    click.echo(msg_welcome)
    if click.confirm('Do you want to continue?'):
        oneTime_author = click.prompt('\nauthor', default=default_author)
        oneTime_mail = click.prompt('author_email', default=default_mail)
        do.config.write_json(oneTime_author, oneTime_mail)


def lice(num, setup_author, project_name):
    """
    Returns the license choosed by the user.
    """
    choose = do.licenses.choose
    return {'1':lambda : choose('Apache License 2.0', setup_author), 
     '2':lambda : choose('BSD License', setup_author), 
     '3':lambda : choose('GNU Affero General Public License v3', setup_author), 
     '4':lambda : choose('GNU Lesser General Public License v3', setup_author), 
     '5':lambda : choose('GNU General Public License v3', setup_author, project_name), 
     '6':lambda : choose('MIT License', setup_author), 
     '7':lambda : choose('Mozilla Public License Version 2.0'), 
     '8':lambda : do.licenses.choose('Unlicensed')}.get(num, lambda : sys.exit(1))()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()