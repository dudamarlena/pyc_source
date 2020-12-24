# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michaeljenny/datashackle/pyramidapp/pyramidapp/views.py
# Compiled at: 2012-08-12 08:19:05
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import DBSession, MyModel

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'one': one, 'project': 'pyramidapp'}


conn_err_msg = 'Pyramid is having a problem using your SQL database.  The problem\nmight be caused by one of the following things:\n\n1.  You may need to run the "initialize_pyramidapp_db" script\n    to initialize your database tables.  Check your virtual \n    environment\'s "bin" directory for this script and try to run it.\n\n2.  Your database server may not be running.  Check that the\n    database server referred to by the "sqlalchemy.url" setting in\n    your "development.ini" file is running.\n\nAfter you fix the problem, please restart the Pyramid application to\ntry it again.\n'