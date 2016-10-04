"""Unit tests for dataset_io.loader module.
"""
from collections import defaultdict
import json
import random
import StringIO
import unittest

from dataset_io import loader
from dataset_io.helper import normalize_rating

from tests.mock import Graph


class TestLoad(unittest.TestCase):
    """Test case for load method.
    """

    def setUp(self):
        """Create a sample graph and its JSON data.
        """
        self.reviews = defaultdict(dict)
        self.size = 0

        buf = StringIO.StringIO()
        for r in range(10):
            for p in range(5):
                if random.random() > 0.5:
                    member_id = "r{0}".format(r)
                    product_id = "p{0}".format(p)
                    rating = random.randint(1, 5)
                    self.reviews[member_id][
                        product_id] = normalize_rating(rating)
                    self.size += 1
                    json.dump({
                        "member_id": member_id,
                        "product_id": product_id,
                        "rating": rating,
                        "date": "2014-01-01"
                    }, buf)
                    buf.write("\n")
        self.input = buf.getvalue().split("\n")

    def test_without_anomalous(self):
        """Test load method without specifying default anomalous score.
        """
        g = loader.load(Graph(), self.input)
        self.assertEqual(len(g.review), self.size)
        for r in g.review:
            self.assertIn(r.member_id, self.reviews)
            self.assertIn(r.product_id, self.reviews[r.member_id])
            self.assertAlmostEqual(
                r.rating, self.reviews[r.member_id][r.product_id])

    def test_with_anomalous(self):
        """Test load method with specifying default anomalous score.
        """
        anomalous = 0.42
        g = loader.load(Graph(), self.input, anomalous)
        self.assertEqual(len(g.review), self.size)
        for r in g.review:
            self.assertIn(r.member_id, self.reviews)
            self.assertIn(r.product_id, self.reviews[r.member_id])
            self.assertAlmostEqual(
                r.rating, self.reviews[r.member_id][r.product_id])
        for r in g.reviewers:
            self.assertEqual(r.anomalous_score, anomalous)


if __name__ == "__main__":
    unittest.main()
