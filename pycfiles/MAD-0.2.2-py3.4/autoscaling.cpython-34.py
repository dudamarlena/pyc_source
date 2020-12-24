# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\autoscaling.py
# Compiled at: 2016-03-31 03:21:33
# Size of source mod 2**32: 2064 bytes


class Rule:

    def __init__(self, guard, action):
        self.guard = guard
        self.action = action

    def applies_to(self, utilisation):
        return self.guard(utilisation)

    def compute(self, count):
        return self.action(count)


class AutoScalingStrategy:

    def __init__(self, minimum, maximum, lower_bound, upper_bound):
        self._minimum = minimum
        self._maximum = maximum
        self._rules = [
         Rule(lambda utilisation: utilisation < lower_bound, lambda count: count - 1),
         Rule(lambda utilisation: utilisation > upper_bound, lambda count: count + 1)]

    def adjust(self, service):
        assert service, "Invalid service (found '%s')" % service
        utilisation = service.utilisation
        worker_count = service.worker_count

        def update():
            for any_rule in self._rules:
                if any_rule.applies_to(utilisation):
                    return any_rule.compute(worker_count)

            return worker_count

        def filter(worker_count):
            if self._minimum <= worker_count <= self._maximum:
                return worker_count
            return service.worker_count

        def set(new_value):
            service.set_worker_count(new_value)

        set(filter(update()))