# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/mturk/qualification.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6974 bytes


class Qualifications(object):

    def __init__(self, requirements=None):
        if requirements is None:
            requirements = []
        self.requirements = requirements

    def add(self, req):
        self.requirements.append(req)

    def get_as_params(self):
        params = {}
        assert len(self.requirements) <= 10
        for n, req in enumerate(self.requirements):
            reqparams = req.get_as_params()
            for rp in reqparams:
                params['QualificationRequirement.%s.%s' % (n + 1, rp)] = reqparams[rp]

        return params


class Requirement(object):
    __doc__ = '\n    Representation of a single requirement\n    '

    def __init__(self, qualification_type_id, comparator, integer_value=None, required_to_preview=False):
        self.qualification_type_id = qualification_type_id
        self.comparator = comparator
        self.integer_value = integer_value
        self.required_to_preview = required_to_preview

    def get_as_params(self):
        params = {'QualificationTypeId': self.qualification_type_id, 
         'Comparator': self.comparator}
        if self.comparator != 'Exists':
            if self.integer_value is not None:
                params['IntegerValue'] = self.integer_value
        if self.required_to_preview:
            params['RequiredToPreview'] = 'true'
        return params


class PercentAssignmentsSubmittedRequirement(Requirement):
    __doc__ = '\n    The percentage of assignments the Worker has submitted, over all assignments the Worker has accepted. The value is an integer between 0 and 100.\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(PercentAssignmentsSubmittedRequirement, self).__init__(qualification_type_id='00000000000000000000', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)


class PercentAssignmentsAbandonedRequirement(Requirement):
    __doc__ = '\n    The percentage of assignments the Worker has abandoned (allowed the deadline to elapse), over all assignments the Worker has accepted. The value is an integer between 0 and 100.\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(PercentAssignmentsAbandonedRequirement, self).__init__(qualification_type_id='00000000000000000070', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)


class PercentAssignmentsReturnedRequirement(Requirement):
    __doc__ = '\n    The percentage of assignments the Worker has returned, over all assignments the Worker has accepted. The value is an integer between 0 and 100.\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(PercentAssignmentsReturnedRequirement, self).__init__(qualification_type_id='000000000000000000E0', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)


class PercentAssignmentsApprovedRequirement(Requirement):
    __doc__ = '\n    The percentage of assignments the Worker has submitted that were subsequently approved by the Requester, over all assignments the Worker has submitted. The value is an integer between 0 and 100.\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(PercentAssignmentsApprovedRequirement, self).__init__(qualification_type_id='000000000000000000L0', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)


class PercentAssignmentsRejectedRequirement(Requirement):
    __doc__ = '\n    The percentage of assignments the Worker has submitted that were subsequently rejected by the Requester, over all assignments the Worker has submitted. The value is an integer between 0 and 100.\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(PercentAssignmentsRejectedRequirement, self).__init__(qualification_type_id='000000000000000000S0', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)


class NumberHitsApprovedRequirement(Requirement):
    __doc__ = '\n    Specifies the total number of HITs submitted by a Worker that have been approved. The value is an integer greater than or equal to 0.\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(NumberHitsApprovedRequirement, self).__init__(qualification_type_id='00000000000000000040', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)


class LocaleRequirement(Requirement):
    __doc__ = "\n    A Qualification requirement based on the Worker's location. The Worker's location is specified by the Worker to Mechanical Turk when the Worker creates his account.\n    "

    def __init__(self, comparator, locale, required_to_preview=False):
        super(LocaleRequirement, self).__init__(qualification_type_id='00000000000000000071', comparator=comparator, integer_value=None, required_to_preview=required_to_preview)
        self.locale = locale

    def get_as_params(self):
        params = {'QualificationTypeId': self.qualification_type_id, 
         'Comparator': self.comparator, 
         'LocaleValue.Country': self.locale}
        if self.required_to_preview:
            params['RequiredToPreview'] = 'true'
        return params


class AdultRequirement(Requirement):
    __doc__ = '\n    Requires workers to acknowledge that they are over 18 and that they agree to work on potentially offensive content. The value type is boolean, 1 (required), 0 (not required, the default).\n    '

    def __init__(self, comparator, integer_value, required_to_preview=False):
        super(AdultRequirement, self).__init__(qualification_type_id='00000000000000000060', comparator=comparator, integer_value=integer_value, required_to_preview=required_to_preview)