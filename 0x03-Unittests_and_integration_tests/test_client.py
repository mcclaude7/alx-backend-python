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

    def test_public_repos_url(self):
        """Test that GithubOrgClient._public_repos_url returns the correct value"""
        # Arrange
        org_name = "test_org"
        expected_repos_url = "https://api.github.com/orgs/test_org/repos"
        mocked_payload = {"repos_url": expected_repos_url}
        
        # Act & Assert
        with patch('client.GithubOrgClient.org', new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = mocked_payload
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            
            # Assert
            self.assertEqual(result, expected_repos_url)
            mock_org.assert_called_once()


if __name__ == '__main__':
    unittest.main()