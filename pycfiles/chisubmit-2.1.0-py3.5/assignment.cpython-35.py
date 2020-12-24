# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/client/assignment.py
# Compiled at: 2020-01-15 11:47:40
# Size of source mod 2**32: 7769 bytes
from chisubmit.client.types import ChisubmitAPIObject, Attribute, APIStringType, APIIntegerType, APIDateTimeType, APIDecimalType, APIBooleanType, APIObjectType, APIListType, Relationship, APITimeDeltaType

class RubricComponent(ChisubmitAPIObject):
    _api_attributes = {'url': Attribute(name='url', attrtype=APIStringType, editable=False), 
     
     'id': Attribute(name='id', attrtype=APIIntegerType, editable=False), 
     
     'description': Attribute(name='name', attrtype=APIStringType, editable=True), 
     
     'order': Attribute(name='order', attrtype=APIIntegerType, editable=True), 
     
     'points': Attribute(name='points', attrtype=APIDecimalType, editable=True)}
    _api_relationships = {}


class Assignment(ChisubmitAPIObject):
    _api_attributes = {'assignment_id': Attribute(name='assignment_id', attrtype=APIStringType, editable=True), 
     
     'name': Attribute(name='name', attrtype=APIStringType, editable=True), 
     
     'deadline': Attribute(name='deadline', attrtype=APIDateTimeType, editable=True), 
     
     'grace_period': Attribute(name='grace_period', attrtype=APITimeDeltaType, editable=True), 
     
     'min_students': Attribute(name='min_students', attrtype=APIIntegerType, editable=True), 
     
     'max_students': Attribute(name='max_students', attrtype=APIIntegerType, editable=True), 
     
     'gradescope_id': Attribute(name='gradescope_id', attrtype=APIIntegerType, editable=True), 
     
     'expected_files': Attribute(name='expected_files', attrtype=APIStringType, editable=True)}
    _api_relationships = {'rubric': Relationship(name='instructors', reltype=APIObjectType(RubricComponent))}

    def get_rubric_components(self):
        """
        :calls: GET /courses/:course/assignments/:assignment/rubric
        :rtype: List of :class:`chisubmit.client.assignment.RubricComponent`
        """
        rubric_components = self.get_related('rubric')
        return rubric_components

    def create_rubric_component(self, description, points, order=None):
        """
        :calls: POST /courses/:course/assignments/:assignment/rubric/
        :param description: string
        :param points: float
        :param order: int
        :rtype: :class:`chisubmit.client.assignment.RubricComponent`
        """
        assert isinstance(description, (str, str)), description
        post_data = {'description': description, 
         'points': points}
        if order is not None:
            post_data['order'] = order
        headers, data = self._api_client._requester.request('POST', self.rubric_url, data=post_data)
        return RubricComponent(self._api_client, headers, data)

    def register(self, students):
        """
        :calls: POST /courses/:course/assignments/:assignment/register
        :param students: list of string
        :rtype: :class:`chisubmit.client.assignment.RegistrationResponse`
        """
        assert isinstance(students, (list, tuple)), students
        post_data = {'students': students}
        headers, data = self._api_client._requester.request('POST', self.url + '/register', data=post_data)
        return RegistrationResponse(self._api_client, headers, data)


class RegistrationResponse(ChisubmitAPIObject):
    _api_attributes = {'new_team': Attribute(name='new_team', attrtype=APIBooleanType, editable=False), 
     
     'team': Attribute(name='team', attrtype=APIObjectType('chisubmit.client.team.Team'), editable=False), 
     
     'team_members': Attribute(name='team_members', attrtype=APIListType(APIObjectType('chisubmit.client.team.TeamMember')), editable=False), 
     
     'registration': Attribute(name='registration', attrtype=APIObjectType('chisubmit.client.team.Registration'), editable=False)}
    _api_relationships = {}