# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\views\userrole.py
# Compiled at: 2020-05-08 05:18:08
# Size of source mod 2**32: 15663 bytes
"""
userrole - manage application users and roles
====================================================
"""
from validators.slug import slug
from validators.email import email
from flask import g, request
from flask_security.recoverable import send_reset_password_instructions
from . import bp
from loutilities.user.model import db, User, Role, Interest, Application
from loutilities.tables import DbCrudApiRolePermissions, get_request_action, SEPARATOR
user_dbattrs = 'id,email,name,given_name,roles,interests,last_login_at,current_login_at,last_login_ip,current_login_ip,login_count,active'.split(',')
user_formfields = 'rowid,email,name,given_name,roles,interests,last_login_at,current_login_at,last_login_ip,current_login_ip,login_count,active'.split(',')
user_dbmapping = dict(zip(user_dbattrs, user_formfields))
user_formmapping = dict(zip(user_formfields, user_dbattrs))

def user_validate(action, formdata):
    results = []
    if formdata['email']:
        if not email(formdata['email']):
            results.append({'name':'email',  'status':'invalid email: correct format is like john.doe@example.com'})
    apps = set()
    if formdata['roles']:
        if 'id' in formdata['roles']:
            if formdata['roles']['id'] != '':
                roleidsstring = formdata['roles']['id']
                roleids = roleidsstring.split(SEPARATOR)
                for roleid in roleids:
                    thisrole = Role.query.filter_by(id=roleid).one()
                    apps |= set(thisrole.applications)

    if g.loutility not in apps:
        results.append({'name':'roles.id',  'status':'give user at least one role which works for this application'})
    return results


class UserCrudApi(DbCrudApiRolePermissions):

    def editor_method_posthook(self, form):
        """
        send new users a link to set their password

        :param form: edit form
        :return: None
        """
        action = get_request_action(form)
        if action == 'create':
            user = User.query.filter_by(id=(self.created_id)).one()
            send_reset_password_instructions(user)

    def updaterow(self, thisid, formdata):
        if 'resetpw' in request.form:
            user = User.query.filter_by(id=thisid).one()
            send_reset_password_instructions(user)
        return super().updaterow(thisid, formdata)


class UserView(UserCrudApi):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(app=bp,
          db=db,
          model=User,
          version_id_col='version_id',
          roles_accepted='super-admin',
          template='datatables.jinja2',
          pagename='users',
          endpoint='userrole.users',
          rule='/users',
          dbmapping=user_dbmapping,
          formmapping=user_formmapping,
          clientcolumns=[
         {'data':'email', 
          'name':'email',  'label':'Email',  '_unique':True,  'className':'field_req'},
         {'data':'given_name', 
          'name':'given_name',  'label':'First Name',  'className':'field_req'},
         {'data':'name', 
          'name':'name',  'label':'Full Name',  'className':'field_req'},
         {'data':'roles', 
          'name':'roles',  'label':'Roles',  '_treatment':{'relationship': {'fieldmodel':Role,  'labelfield':'name',  'formfield':'roles',  'dbfield':'roles', 
                            'uselist':True}}},
         {'data':'interests', 
          'name':'interests',  'label':'Interests',  '_treatment':{'relationship': {'fieldmodel':Interest,  'labelfield':'description',  'formfield':'interests', 
                            'dbfield':'interests',  'uselist':True}}},
         {'data':'active', 
          'name':'active',  'label':'Active',  '_treatment':{'boolean': {'formfield':'active',  'dbfield':'active'}}, 
          'ed':{'def': 'yes'}},
         {'data':'last_login_at', 
          'name':'last_login_at',  'label':'Last Login At',  'type':'readonly'},
         {'data':'current_login_at', 
          'name':'current_login_at',  'label':'Current Login At',  'type':'readonly'},
         {'data':'last_login_ip', 
          'name':'last_login_ip',  'label':'Last Login IP',  'type':'readonly'},
         {'data':'current_login_ip', 
          'name':'current_login_ip',  'label':'Current Login IP',  'type':'readonly'},
         {'data':'login_count', 
          'name':'login_count',  'label':'Login Count',  'type':'readonly'}],
          validate=user_validate,
          servercolumns=None,
          idSrc='rowid',
          buttons=[
         'create',
         {'extend':'editRefresh', 
          'text':'Edit', 
          'editor':{'eval': 'editor'}, 
          'formButtons':[
           {'text':'Reset Password', 
            'action':{'eval': 'reset_password_button'}},
           {'text':'Update', 
            'action':{'eval': 'submit_button'}}]}],
          dtoptions={'scrollCollapse':True, 
         'scrollX':True, 
         'scrollXInner':'100%', 
         'scrollY':True})
        args.update(kwargs)
        (super().__init__)(**args)


role_dbattrs = 'id,name,description,applications'.split(',')
role_formfields = 'rowid,name,description,applications'.split(',')
role_dbmapping = dict(zip(role_dbattrs, role_formfields))
role_formmapping = dict(zip(role_formfields, role_dbattrs))

class RoleView(DbCrudApiRolePermissions):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(app=bp,
          db=db,
          model=Role,
          version_id_col='version_id',
          roles_accepted='super-admin',
          template='datatables.jinja2',
          pagename='roles',
          endpoint='userrole.roles',
          rule='/roles',
          dbmapping=role_dbmapping,
          formmapping=role_formmapping,
          clientcolumns=[
         {'data':'name', 
          'name':'name',  'label':'Name',  'className':'field_req'},
         {'data':'description', 
          'name':'description',  'label':'Description'},
         {'data':'applications', 
          'name':'applications',  'label':'Applications',  '_treatment':{'relationship': {'fieldmodel':Application,  'labelfield':'application',  'formfield':'applications', 
                            'dbfield':'applications',  'uselist':True}}}],
          servercolumns=None,
          idSrc='rowid',
          buttons=[
         'create', 'editRefresh', 'remove'],
          dtoptions={'scrollCollapse':True, 
         'scrollX':True, 
         'scrollXInner':'100%', 
         'scrollY':True})
        args.update(kwargs)
        (super().__init__)(**args)


interest_dbattrs = 'id,interest,description,users,public,applications'.split(',')
interest_formfields = 'rowid,interest,description,users,public,applications'.split(',')
interest_dbmapping = dict(zip(interest_dbattrs, interest_formfields))
interest_formmapping = dict(zip(interest_formfields, interest_dbattrs))

def interest_validate(action, formdata):
    results = []
    for field in ('interest', ):
        if formdata[field] and not slug(formdata[field]):
            results.append({'name':field,  'status':'invalid slug: must be only alpha, numeral, hyphen'})

    return results


class InterestView(DbCrudApiRolePermissions):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        args = dict(app=bp,
          db=db,
          model=Interest,
          version_id_col='version_id',
          interests_accepted='super-admin',
          template='datatables.jinja2',
          pagename='interests',
          endpoint='userrole.interests',
          rule='/interests',
          dbmapping=interest_dbmapping,
          formmapping=interest_formmapping,
          clientcolumns=[
         {'data':'description', 
          'name':'description',  'label':'Description',  '_unique':True,  'className':'field_req'},
         {'data':'interest', 
          'name':'interest',  'label':'Slug',  '_unique':True,  'className':'field_req'},
         {'data':'public', 
          'name':'public',  'label':'Public',  '_treatment':{'boolean': {'formfield':'public',  'dbfield':'public'}}, 
          'ed':{'def': 'yes'}},
         {'data':'applications', 
          'name':'applications',  'label':'Applications',  '_treatment':{'relationship': {'fieldmodel':Application,  'labelfield':'application',  'formfield':'applications', 
                            'dbfield':'applications',  'uselist':True}}},
         {'data':'users', 
          'name':'users',  'label':'Users',  '_treatment':{'relationship': {'fieldmodel':User,  'labelfield':'email',  'formfield':'users', 
                            'dbfield':'users',  'uselist':True}}}],
          validate=interest_validate,
          servercolumns=None,
          idSrc='rowid',
          buttons=[
         'create', 'editRefresh', 'remove'],
          dtoptions={'scrollCollapse':True, 
         'scrollX':True, 
         'scrollXInner':'100%', 
         'scrollY':True})
        args.update(kwargs)
        (super().__init__)(**args)


application_dbattrs = 'id,application'.split(',')
application_formfields = 'rowid,application'.split(',')
application_dbmapping = dict(zip(application_dbattrs, application_formfields))
application_formmapping = dict(zip(application_formfields, application_dbattrs))

def application_validate(action, formdata):
    results = []
    for field in ('application', ):
        if formdata[field] and not slug(formdata[field]):
            results.append({'name':field,  'status':'invalid slug: must be only alpha, numeral, hyphen'})

    return results


application = DbCrudApiRolePermissions(app=bp,
  db=db,
  model=Application,
  version_id_col='version_id',
  applications_accepted='super-admin',
  template='datatables.jinja2',
  pagename='applications',
  endpoint='userrole.applications',
  rule='/applications',
  dbmapping=application_dbmapping,
  formmapping=application_formmapping,
  clientcolumns=[
 {'data':'application', 
  'name':'application',  'label':'Application',  '_unique':True,  'className':'field_req'}],
  validate=application_validate,
  servercolumns=None,
  idSrc='rowid',
  buttons=[
 'create', 'editRefresh', 'remove'],
  dtoptions={'scrollCollapse':True, 
 'scrollX':True, 
 'scrollXInner':'100%', 
 'scrollY':True})
application.register()