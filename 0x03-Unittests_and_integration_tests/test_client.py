#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Arrange
        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_result = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        
        # Configure mock
        mock_get_json.return_value = expected_result
        
        # Act
        client = GithubOrgClient(org_name)
        result = client.org
        
        # Assert
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()