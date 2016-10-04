# pylint: disable=protected-access
"""Unit tests for dataset_io.sampler module.
"""
from __future__ import division
from collections import defaultdict
import itertools
import unittest

from dataset_io.helper import normalize_rating
from dataset_io.sampler import UniformSampler
from dataset_io.sampler import RatingBasedSampler


class TestUniformSampler(unittest.TestCase):
    """Test case for UniformSampler class.
    """

    def test(self):
        """Test the correctness by comparing max and min appearance.
        """
        counter = defaultdict(int)
        size = 100000
        sampler = UniformSampler()
        for s in itertools.islice(sampler(), size):
            counter[s] += 1

        error = max(counter.values()) - min(counter.values())
        self.assertLess(error, size * 0.01)  # Less than 1%.


class TestRatingBasedSampler(unittest.TestCase):
    """Test case for RatingBasedSampler class.
    """

    def test(self):
        """Test the correctness by comparing ratios of the original histogram.
        """
        counter = defaultdict(int)
        size = 100000
        sampler = RatingBasedSampler()
        for s in itertools.islice(sampler(), size):
            counter[s] += 1

        ratios = [
            abs(counter[normalize_rating(rating)] / size - value)
            for rating, value in sampler._dist.items()
        ]
        error = max(ratios) - min(ratios)
        self.assertLess(error, size * 0.01)


if __name__ == "__main__":
    unittest.main()
