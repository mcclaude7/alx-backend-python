#!/usr/bin/env python3
"""Unit tests for utlity functions in the utils module."""

import unittest
from utils import access_nested_map
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""
    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a":{"b":2}},("a",),{"b": 2}),
            ({"a":{"b":2}},("a","b"), 2),

        ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == '__main__':
    unittest.main()