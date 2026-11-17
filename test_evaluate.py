import unittest

from evaluate import load_fixtures, run_evaluation


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.results = {
            (result["candidate"], result["fixture"]): result
            for result in run_evaluation(load_fixtures())
        }

    def test_all_candidate_fixture_pairs_are_evaluated(self):
        self.assertEqual(len(self.results), 12)

    def test_only_known_candidate_defects_fail(self):
        failures = {pair for pair, result in self.results.items() if not result["passed"]}
        self.assertEqual(
            failures,
            {
                ("first-row-per-id", "same-id-different-status"),
                ("first-row-per-id", "preserve-whitespace-and-leading-zeros"),
                ("nonempty-rows", "valid-empty-cell"),
            },
        )

    def test_evidence_shows_the_dropped_row(self):
        result = self.results[("first-row-per-id", "same-id-different-status")]
        self.assertIn(("001", "Ari", "closed"), result["expected"])
        self.assertNotIn(("001", "Ari", "closed"), result["actual"])


if __name__ == "__main__":
    unittest.main()
