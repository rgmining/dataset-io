"""Unit tests for dataset_io.resume module.
"""
import StringIO
import random
import unittest

from dataset_io import resume
from dataset_io.helper import normalize_rating
from dataset_io.helper import print_state

from tests.mock import Graph


class TestResume(unittest.TestCase):
    """Test case for resume method.
    """

    def setUp(self):
        """Create a sample graph and its JSON data.
        """
        self.graph = Graph()
        for r in range(10):
            for p in range(5):
                if random.random() > 0.5:
                    member_id = "r{0}".format(r)
                    product_id = "p{0}".format(p)
                    rating = normalize_rating(random.randint(1, 5))

                    self.graph.add_review(
                        self.graph.new_reviewer(member_id, 0.),
                        self.graph.new_product(product_id),
                        rating, "2014-01-01")

    def test(self):
        """Test resume method with a random graph and states.
        """
        output = StringIO.StringIO()

        # Construct a target state.
        anomalous_score = random.random()
        summary = random.random()
        for r in self.graph.reviewers:
            r.anomalous_score = anomalous_score
        for p in self.graph.products:
            p.summary = summary
        print_state(self.graph, 1, output)

        # Update state.
        for i in range(5, 10):
            for r in self.graph.reviewers:
                r.anomalous_score = random.random()
            for p in self.graph.products:
                p.summary = random.random()
            print_state(self.graph, i, output)

        # Restore state.
        g = resume(self.graph, output.getvalue().split("\n"), 1)
        for r in g.reviewers:
            self.assertEqual(r.anomalous_score, anomalous_score)
        for p in g.products:
            self.assertAlmostEqual(p.summary, summary)


if __name__ == "__main__":
    unittest.main()
