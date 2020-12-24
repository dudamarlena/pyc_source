# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims/department.py
# Compiled at: 2018-04-27 18:28:17
# Size of source mod 2**32: 1731 bytes
from trytond.model import ModelView, ModelSQL, fields
__all__ = [
 'Department', 'UserDepartment']

class Department(ModelSQL, ModelView):
    """Department"""
    __name__ = 'company.department'
    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    default_location = fields.Many2One('stock.location', 'Default Location', domain=[
     ('type', '=', 'storage')])


class UserDepartment(ModelSQL, ModelView):
    __doc__ = 'User Department'
    __name__ = 'user.department'
    user = fields.Many2One('res.user', 'User', required=True)
    department = fields.Many2One('company.department', 'Department', required=True)
    default = fields.Boolean('By default')

    @classmethod
    def __setup__(cls):
        super(UserDepartment, cls).__setup__()
        cls._error_messages.update({'default_department': 'There is already a default department for this user'})

    @staticmethod
    def default_default():
        return False

    @classmethod
    def validate(cls, user_departments):
        super(UserDepartment, cls).validate(user_departments)
        for ud in user_departments:
            ud.check_default()

    def check_default(self):
        if self.default:
            user_departments = self.search([
             (
              'user', '=', self.user.id),
             ('default', '=', True),
             (
              'id', '!=', self.id)])
            if user_departments:
                self.raise_user_error('default_department')