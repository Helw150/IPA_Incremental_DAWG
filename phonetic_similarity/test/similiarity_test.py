from libs.phonetic_similarity import similarity
from libs.phonetic_similarity import data
import unittest

import random


class DistanceTest(unittest.TestCase):
    def test_get_vector(self):
        with self.assertRaises(ValueError):
            similarity._get_vector("")
            similarity._get_vector("&")
        self.assertEqual(data.phone_features["c"], similarity._get_vector("c"))
        self.assertEqual(similarity._get_vector("tʃ"),
                         [False, False, True, True, False, False, False, True,
                          False, False, False, True, True, True, False, False,
                          False, False, False, None, False])
        self.assertEqual(similarity._get_vector("aː"),
                         [True, True, False, True, False, False, False, None,
                          True, False, False, False, False, False, False,
                          False, True, True, False, True, True])

    def test_similarity(self):
        self.assertEqual(similarity.similarity("a", "a"), 1)
        self.assertTrue(abs(similarity.similarity("b", "p") -
                            0.9807692307692307) < 1e-6)
        self.assertTrue(abs(similarity.similarity("a", "aː") -
                            0.9818181818181819) < 1e-6)
        self.assertTrue(abs(similarity.similarity("b", "p", weighted=False) -
                            0.9444444444444446) < 1e-6)
        self.assertTrue(abs(similarity.similarity("a", "aː", weighted=False) -
                            0.95) < 1e-6)


def benchmark():
    phones = list(data.phone_features.keys())
    count = 0
    for i in range(10000):
        seqA = []
        seqB = []
        for i in range(10):
            phoneA = random.choice(phones)
            phoneB = random.choice(phones)
            seqA.append(phoneA)
            seqB.append(phoneB)
        for phoneA in seqA:
            for phoneB in seqB:
                similarity.similarity(phoneA, phoneB)
                count += 1
    print(count)


if __name__ == "__main__":
    unittest.main()
    # benchmark()
