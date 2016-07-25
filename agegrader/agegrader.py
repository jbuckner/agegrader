from __future__ import division
import json
import operator

from .utils import kilometers_to_miles


class AgeGrader(object):
    """
    This calculates age graded performance, finish times, and paces.

    It uses an estimation method to adjust for missing data points. For
    instance, there is no data for 4.5-mile races. There are 4 and 5-mile
    tables, though. Using them, this finds the distance delta between available
    data and based on that percentage, estimates the world record for the given
    distance.

    Usage:

    age_grader = AgeGrader(age, gender, km)

    age_grader.age_graded_performance_factor
    - the age graded performance factor as a decimal (.83 = 83%)

    age_grader.age_graded_finish_time
    - the age graded finish time in seconds

    age_grader.age_graded_page
    - the age graded pace in seconds per mile

    age_grader.age_gender_distance_record
    - returns the adjusted record for the given age, gender, and distance

    age_grader.gender_distance_record
    - this is the "world record" for the distance
    - returns the adjusted record for the given gender and distance
    """
    def __init__(self, age, gender, km, seconds):
        super(AgeGrader, self).__init__()
        self.age = age
        self.gender = gender
        self.distance_in_km = km
        self.seconds = seconds
        with open('agegrader/age_grading_data.json') as data_file:
            self.age_grading_data = json.load(data_file)

    @property
    def age_graded_performance_factor(self):
        """
        Age-graded performance factor as a decimal. For instance .83 = 83%

        """
        return self.age_gender_distance_record / self.seconds

    @property
    def age_graded_finish_time(self):
        """
        Age-graded finish time in seconds

        """
        return self.gender_distance_record / self.age_graded_performance_factor

    @property
    def age_graded_seconds_per_mile(self):
        """
        Age-graded pace in seconds per mile

        """
        miles = kilometers_to_miles(self.distance_in_km)
        seconds_per_mile = self.age_graded_finish_time / miles
        return seconds_per_mile

    @property
    def age_gender_distance_record(self):
        """
        World record in seconds for given age, gender, and distance

        """
        lower_ages = self.__next_lower_distance['ages']
        higher_ages = self.__next_higher_distance['ages']

        lower_age = (
            item for item in lower_ages if item['age'] == self.age).next()
        higher_age = (
            item for item in higher_ages if item['age'] == self.age).next()

        lower_seconds = lower_age['seconds']
        higher_seconds = higher_age['seconds']
        diff = higher_seconds - lower_seconds
        adjusted = lower_seconds + (diff * self.__distance_ratio)
        return adjusted

    @property
    def gender_distance_record(self):
        """
        World record in seconds for given gender and distance.

        """
        lower_record = self.__next_lower_distance.seconds
        upper_record = self.__next_higher_distance.seconds
        diff = upper_record - lower_record
        delta = self.__distance_ratio * diff
        value = lower_record + delta
        return value

    @property
    def __next_higher_distance(self):
        """
        The next greater or equal distance from km.

        """
        self.age_grading_data.sort(key=operator.itemgetter('distance'))
        for distance in self.age_grading_data:
            if distance['distance'] >= self.distance_in_km:
                return distance
        return self.age_grading_data[-1]

    @property
    def __next_lower_distance(self):
        """
        The next lower or equal distance from km.

        """
        self.age_grading_data.sort(key=operator.itemgetter('distance'),
                                   reverse=True)
        for distance in self.age_grading_data:
            if distance['distance'] <= self.distance_in_km:
                return distance
        return self.age_grading_data[-1]

    @property
    def __distance_ratio(self):
        """
        The distance ratio of km between upper_distance and lower_distance

        For instance, given 7.5km where we have 5km and 10km tables, 7.5km
        is 50-percent between 5 and 10 so this returns 0.5

        This is used to adjust the record times for these distances. For
        instance, for a 35-year-old male, the 5k record is 796 seconds and
        for a 10k, it's 1618. 1618 - 796 = 822 * 0.5 = 411 + 796 = 1207.

        The adjusted record for 7.5km would be 1207 seconds. This is a simple
        example, but you get the idea.

        """
        lower_distance = self.__next_lower_distance['distance']
        upper_distance = self.__next_higher_distance['distance']
        diff = upper_distance - lower_distance
        if diff == 0:
            return 0
        delta = self.distance_in_km - lower_distance
        ratio = delta / diff
        return ratio
