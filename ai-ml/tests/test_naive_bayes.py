import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from naive_bayes import train_naive_bayes, predict_naive_bayes


class NaiveBayesTestCase(unittest.TestCase):
    def test_train_and_predict(self):
        texts = ["hello world", "server error", "hello again"]
        labels = [1, 0, 1]
        model = train_naive_bayes(texts, labels)

        self.assertEqual(model["total_docs"], 3)
        prediction = predict_naive_bayes(model, "hello")
        self.assertIn(prediction, [0, 1])


if __name__ == "__main__":
    unittest.main()
