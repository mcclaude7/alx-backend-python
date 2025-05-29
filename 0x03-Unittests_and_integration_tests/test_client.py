# #!/usr/bin/env python3
# """Unit tests for GithubOrgClient class"""

# import unittest
# from unittest.mock import patch
# from parameterized import parameterized
# from client import GithubOrgClient


# class TestGithubOrgClient(unittest.TestCase):
#     """Test case for GithubOrgClient"""

#     @parameterized.expand([
#         ("google",),
#         ("abc",),
#     ])
#     @patch('client.get_json')
#     def test_org(self, org_name, mock_get_json):
#         """Test that GithubOrgClient.org returns the correct value"""
#         expected_url = f"https://api.github.com/orgs/{org_name}"
#         expected_result = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        
#         mock_get_json.return_value = expected_result
        
#         client = GithubOrgClient(org_name)
#         result = client.org
        
#         mock_get_json.assert_called_once_with(expected_url)
#         self.assertEqual(result, expected_result)

#     def test_public_repos_url(self):
#         """Test that GithubOrgClient._public_repos_url returns the correct value"""
#         org_name = "test_org"
#         expected_repos_url = "https://api.github.com/orgs/test_org/repos"
#         mocked_payload = {"repos_url": expected_repos_url}
        
#         with patch('client.GithubOrgClient.org',
#                   new_callable=unittest.mock.PropertyMock) as mock_org:
#             mock_org.return_value = mocked_payload
#             client = GithubOrgClient(org_name)
#             result = client._public_repos_url
            
#             self.assertEqual(result, expected_repos_url)
#             mock_org.assert_called_once()

#     @patch('client.get_json')
#     def test_public_repos(self, mock_get_json):
#         """Test that GithubOrgClient.public_repos returns the correct list of repos"""
#         org_name = "test_org"
#         test_repos_url = "https://api.github.com/orgs/test_org/repos"
#         test_payload = [
#             {"name": "repo1", "license": {"key": "mit"}},
#             {"name": "repo2", "license": {"key": "apache-2.0"}},
#             {"name": "repo3", "license": None}
#         ]
#         expected_repos = ["repo1", "repo2", "repo3"]
        
#         mock_get_json.return_value = test_payload
        
#         with patch('client.GithubOrgClient._public_repos_url',
#                   new_callable=unittest.mock.PropertyMock) as mock_public_repos_url:
#             mock_public_repos_url.return_value = test_repos_url
#             client = GithubOrgClient(org_name)
#             result = client.public_repos()
            
#             self.assertEqual(result, expected_repos)
#             mock_public_repos_url.assert_called_once()
#             mock_get_json.assert_called_once_with(test_repos_url)


# if __name__ == '__main__':
#     unittest.main()
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
        expected_url = f"https://api.github.com/orgs/{org_name}"
        expected_result = {
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
        }
        
        mock_get_json.return_value = expected_result
        
        client = GithubOrgClient(org_name)
        result = client.org
        
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_result)

    def test_public_repos_url(self):
        """Test that GithubOrgClient._public_repos_url returns the correct value"""
        org_name = "test_org"
        expected_repos_url = "https://api.github.com/orgs/test_org/repos"
        mocked_payload = {"repos_url": expected_repos_url}
        
        with patch('client.GithubOrgClient.org',
                   new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = mocked_payload
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            
            self.assertEqual(result, expected_repos_url)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns the correct list of repos"""
        org_name = "test_org"
        test_repos_url = "https://api.github.com/orgs/test_org/repos"
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        expected_repos = ["repo1", "repo2", "repo3"]
        
        mock_get_json.return_value = test_payload
        
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=unittest.mock.PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_repos_url
            client = GithubOrgClient(org_name)
            result = client.public_repos()
            
            self.assertEqual(result, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)


if __name__ == '__main__':
    unittest.main()
