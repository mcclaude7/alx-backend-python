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
    
    @parameterized.expand([
        ({}, ("a"), "a"),
        ({"a" : 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that access_nested_map raises a key Error when the path doesn't exist """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")

if __name__ == '__main__':
    unittest.main()