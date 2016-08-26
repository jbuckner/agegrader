from __future__ import division
import json
import os

from .utils import (next_highest_in_list, next_lowest_in_list,
                    kilometers_to_miles)


class AgeGrader(object):
    """
    This calculates age graded performance, finish times, and paces.

    Usage:

    age_grader = AgeGrader()

    age_grader.age_graded_performance_factor(age, gender, distance, seconds)
    - the age graded performance factor as a decimal (.83 = 83%)

    age_grader.age_graded_finish_time(age, gender, distance, seconds)
    - the age graded finish time in seconds

    age_grader.age_graded_seconds_per_mile(age, gender, distance, seconds)
    - the age graded pace in seconds per mile

    age_grader.age_gender_distance_record(age, gender, distance)
    - returns the adjusted record for the given age, gender, and distance

    age_grader.gender_distance_record(gender, distance)
    - this is the "world record" for the distance
    - returns the adjusted record for the given gender and distance

    Advanced Usage:

    Custom data file:

    with open('path/to/custom_data.json') as dat:
        a = AgeGrader(dat)
        a.age_graded_performance_factor(age, gender, distance, seconds)
    """
    def __init__(self, data_file=None):
        super(AgeGrader, self).__init__()
        if data_file:
            self.age_grading_data = json.load(data_file)
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open('{}/age_grading_data.json'.format(dir_path)) as dat:
                self.age_grading_data = json.load(dat)
        self.distances = list(set([entry['distance'] for entry
                                   in self.age_grading_data]))

    def age_graded_performance_factor(self, age, gender, distance, seconds):
        """
        Age-graded performance factor as a decimal. For instance .83 = 83%

        Returns None if age data not available

        """
        age_gender_distance_record = self.age_gender_distance_record(
            age, gender, distance)
        if age_gender_distance_record:
            return age_gender_distance_record / seconds
        return None

    def age_graded_finish_time(self, age, gender, distance, seconds):
        """
        Age-graded finish time in seconds

        Returns None if age data not available

        """
        gdr = self.gender_distance_record(gender, distance)
        agpf = self.age_graded_performance_factor(age, gender, distance,
                                                  seconds)
        if agpf:
            return gdr / agpf
        return None

    def age_graded_seconds_per_mile(self, age, gender, distance, seconds):
        """
        Age-graded pace in seconds per mile

        Returns None if age data not available

        """
        miles = kilometers_to_miles(distance)
        agft = self.age_graded_finish_time(age, gender, distance, seconds)
        if agft:
            seconds_per_mile = agft / miles
            return seconds_per_mile
        return None

    def age_gender_distance_record(self, age, gender, distance):
        """
        World record in seconds for given age, gender, and distance

        Returns None if age data not available

        """
        lower_gender_distance = self.__lower_distance_entry(gender, distance)
        higher_gender_distance = self.__higher_distance_entry(gender, distance)

        lower_ages = lower_gender_distance['ages']
        higher_ages = higher_gender_distance['ages']

        lower_age = list(item for item in lower_ages if item['age'] == age)
        higher_age = list(item for item in higher_ages if item['age'] == age)

        if len(lower_age) is 0 or len(higher_age) is 0:
            return None

        lower_seconds = lower_age[0]['seconds']
        higher_seconds = higher_age[0]['seconds']
        diff = higher_seconds - lower_seconds
        distance_ratio = self.__distance_ratio(distance)
        adjusted = lower_seconds + (diff * distance_ratio)
        return adjusted

    def gender_distance_record(self, gender, distance):
        """
        World record in seconds for given gender and distance.

        """
        lower_gender_distance = self.__lower_distance_entry(gender, distance)
        higher_gender_distance = self.__higher_distance_entry(gender, distance)

        lower_record = lower_gender_distance['seconds']
        upper_record = higher_gender_distance['seconds']

        diff = upper_record - lower_record
        delta = self.__distance_ratio(distance) * diff
        value = lower_record + delta
        return value

    def __higher_distance_entry(self, gender, distance):
        """
        Return the next highest entry from the data

        """
        next_higher_distance = self.__next_higher_distance(distance)
        higher_gender_distance = self.__gender_distance_entry(
            gender, next_higher_distance)
        return higher_gender_distance

    def __lower_distance_entry(self, gender, distance):
        """
        Return the next lowest entry from the data

        """
        next_lower_distance = self.__next_lower_distance(distance)
        lower_gender_distance = self.__gender_distance_entry(
            gender, next_lower_distance)
        return lower_gender_distance

    def __gender_distance_entry(self, gender, distance):
        """
        Return a gender distance entry from the data

        """
        return next(entry for entry in self.age_grading_data
                    if entry['gender'] == gender.upper() and
                    entry['distance'] == distance)

    def __next_higher_distance(self, distance):
        """
        Return the next highest distance from the list of data points

        """
        return next_highest_in_list(self.distances, distance)

    def __next_lower_distance(self, distance):
        """
        Return the next lowest distance from the list of data points

        """
        return next_lowest_in_list(self.distances, distance)

    def __distance_ratio(self, distance):
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
        lower_distance = self.__next_lower_distance(distance)
        upper_distance = self.__next_higher_distance(distance)
        diff = upper_distance - lower_distance
        if diff == 0:
            return 0
        delta = distance - lower_distance
        ratio = delta / diff
        return ratio
