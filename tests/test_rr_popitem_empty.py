import unittest

import cachetools


class RRCachePopitemEmptyTest(unittest.TestCase):
    def assert_empty_popitem_raises_keyerror(self, choice):
        cache = cachetools.RRCache(maxsize=2, choice=choice)
        with self.assertRaises(KeyError) as cm:
            cache.popitem()
        self.assertEqual("RRCache is empty", cm.exception.args[0])

    def test_min_choice(self):
        self.assert_empty_popitem_raises_keyerror(min)

    def test_max_choice(self):
        self.assert_empty_popitem_raises_keyerror(max)

    def test_next_iter_choice(self):
        self.assert_empty_popitem_raises_keyerror(lambda seq: next(iter(seq)))

    def test_choice_raising_value_error(self):
        def choice(seq):
            raise ValueError("custom")

        self.assert_empty_popitem_raises_keyerror(choice)

    def test_choice_raising_runtime_error(self):
        def choice(seq):
            raise RuntimeError("custom")

        self.assert_empty_popitem_raises_keyerror(choice)

    def test_non_empty_popitem_still_works(self):
        cache = cachetools.RRCache(maxsize=2, choice=min)
        cache[1] = "one"
        cache[2] = "two"
        self.assertEqual((1, "one"), cache.popitem())
        self.assertEqual(1, len(cache))


if __name__ == "__main__":
    unittest.main()
