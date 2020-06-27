from unittest import TestCase
from util import distinct_prefix


class UtilTest(TestCase):
    def test_prefix_generator(self):
        self.assertEqual(distinct_prefix("fankenstein", "frankenwald"), "frankens")
        self.assertEqual(distinct_prefix("fankenwald", "frankenstein"), "frankenw")
        self.assertEqual(distinct_prefix("hello", "world"), "h")
        self.assertEqual(distinct_prefix("hello", "hello"), "hello")
