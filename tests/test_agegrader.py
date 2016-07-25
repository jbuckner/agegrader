# -*- coding: utf-8 -*-

import unittest
from agegrader.agegrader import AgeGrader


class AgeGraderTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_age_grader(self):
        a = AgeGrader(15, 'M', 5.0, 1234)
        rounded = round(a.age_graded_performance_factor, 3)
        assert rounded == 0.654

if __name__ == '__main__':
    unittest.main()
