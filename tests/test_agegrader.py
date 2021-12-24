# -*- coding: utf-8 -*-

import unittest
from agegrader.agegrader import AgeGrader


class AgeGraderTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_age_grader_returns_expected_performance_factor(self):
        a = AgeGrader()
        agfp = a.age_graded_performance_factor(15, 'M', 5.0, 1234)
        rounded = round(agfp, 3)
        assert rounded == 0.654

    def test_age_grader_returns_none_if_age_not_found(self):
        with open('tests/test_data.json') as dat:
            a = AgeGrader(dat)
        agfp = a.age_graded_performance_factor(15, 'M', 5.0, 1234)
        assert agfp is None


if __name__ == '__main__':
    unittest.main()
