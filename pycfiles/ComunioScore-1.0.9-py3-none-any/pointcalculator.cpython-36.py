# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/pointcalculator.py
# Compiled at: 2020-04-27 15:29:14
# Size of source mod 2**32: 3276 bytes
import logging

class PointCalculator:
    """PointCalculator"""

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class PointCalculator')

    @staticmethod
    def get_points_from_rating(rating):
        """ calculates the points from rating

        :param rating: rating number
        :return: points for given rating
        """
        if rating >= 0:
            if rating <= 4.6:
                return -8
            else:
                if rating >= 4.7:
                    if rating <= 4.9:
                        return -7
                    else:
                        if rating >= 5.0:
                            if rating <= 5.2:
                                return -6
                            else:
                                if rating >= 5.3:
                                    if rating <= 5.4:
                                        return -5
                                    else:
                                        if rating >= 5.5:
                                            if rating <= 5.6:
                                                return -4
                                            else:
                                                if rating >= 5.7:
                                                    if rating <= 5.8:
                                                        return -3
                                                    elif rating >= 5.9:
                                                        if rating <= 6.0:
                                                            return -2
                                                    else:
                                                        if rating >= 6.1:
                                                            if rating <= 6.2:
                                                                return -1
                                                        if rating >= 6.3:
                                                            if rating <= 6.4:
                                                                return 0
                                                    if rating >= 6.5 and rating <= 6.6:
                                                        return 1
                                                else:
                                                    if rating >= 6.7:
                                                        if rating <= 6.8:
                                                            return 2
                                                if rating >= 6.9:
                                                    if rating <= 7.0:
                                                        return 3
                                        else:
                                            if rating >= 7.1:
                                                if rating <= 7.2:
                                                    return 4
                                        if rating >= 7.3:
                                            if rating <= 7.4:
                                                return 5
                                else:
                                    if rating >= 7.5:
                                        if rating <= 7.6:
                                            return 6
                                if rating >= 7.7:
                                    if rating <= 7.8:
                                        return 7
                        else:
                            if rating >= 7.9:
                                if rating <= 8.0:
                                    return 8
                        if rating >= 8.1:
                            if rating <= 8.4:
                                return 9
                else:
                    if rating >= 8.5:
                        if rating <= 8.8:
                            return 10
                if rating >= 8.9:
                    if rating <= 9.2:
                        return 11
        else:
            if rating >= 9.3:
                if rating <= 10.0:
                    return 12
        logging.getLogger('ComunioScore').error('Invalid rating {}'.format(rating))

    @staticmethod
    def get_points_for_goal(position):
        """ calculates points for goals

        :param position: position type
        :return: points for the position type
        """
        if position == 'Goalkeeper' or position == 'keeper':
            return 6
        else:
            if position == 'Defender' or position == 'defender':
                return 5
            if position == 'Midfielder' or position == 'midfielder':
                return 4
            if position == 'Forward' or position == 'striker':
                return 3
        logging.getLogger('ComunioScore').error('Invalid position {}'.format(position))

    @staticmethod
    def get_points_for_offs(off_type):
        """ get points for offs

        :return: points for the off type
        """
        if off_type == 'yellow_red':
            return -3
        if off_type == 'red':
            return -6
        logging.getLogger('ComunioScore').error('Invalid off_type {}'.format(off_type))

    @staticmethod
    def get_penalty():
        """ get points for penalty

        :return: points for penalty
        """
        return 3