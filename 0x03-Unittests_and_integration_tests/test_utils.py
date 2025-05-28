#!/usr/bin/env python3
"""Unit tests for utlity functions in the utils module."""

import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch, Mock
import utils

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

class TestGetJson(unittest.TestCase):
    """Test the get_json function from utils.py"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected payload
        and that requests.get is called correctly.
        """
        # Create a mock response object with .json() returning test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Set requests.get to return this mock response
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Verify requests.get was called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Verify get_json returned the expected result
        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Test memoize decorator functionality."""

    def test_memoize(self):
        """Test that memoize caches method result after first call."""

        class TestClass:
            def __init__(self):
                self.called = 0

            def a_method(self):
                self.called += 1
                return 42

            @utils.memoize
            def a_property(self):
                return self.a_method()

        instance = TestClass()

        # Patch a_method to track calls
        with patch.object(instance, 'a_method', wraps=instance.a_method) as mocked_method:
            # Call the property twice
            first = instance.a_property
            second = instance.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            # Ensure a_method was called only once due to memoization
            mocked_method.assert_called_once()



if __name__ == '__main__':
    unittest.main()