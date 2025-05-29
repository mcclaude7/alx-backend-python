# #!/usr/bin/env python3
# """Unit tests for GithubOrgClient class"""

# import unittest
# from unittest.mock import patch, Mock
# from parameterized import parameterized, parameterized_class
# from client import GithubOrgClient
# from fixtures import TEST_PAYLOAD

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
#         expected_result = {
#             "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
#         }
        
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
#                    new_callable=unittest.mock.PropertyMock) as mock_org:
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
#                    new_callable=unittest.mock.PropertyMock) as mock_public_repos_url:
#             mock_public_repos_url.return_value = test_repos_url
#             client = GithubOrgClient(org_name)
#             result = client.public_repos()
            
#             self.assertEqual(result, expected_repos)
#             mock_public_repos_url.assert_called_once()
#             mock_get_json.assert_called_once_with(test_repos_url)

#     @parameterized.expand([
#         ({"license": {"key": "my_license"}}, "my_license", True),
#         ({"license": {"key": "other_license"}}, "my_license", False),
#     ])
#     def test_has_license(self, repo, license_key, expected):
#         """Test that GithubOrgClient.has_license returns the correct value"""
#         client = GithubOrgClient("test_org")
#         result = client.has_license(repo, license_key)
#         self.assertEqual(result, expected)

# @parameterized_class([
#     {
#         'org_payload': TEST_PAYLOAD[0][0],
#         'repos_payload': TEST_PAYLOAD[0][1],
#         'expected_repos': TEST_PAYLOAD[0][2],
#         'apache2_repos': TEST_PAYLOAD[0][3]
#     }
# ])
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration test case for GithubOrgClient"""

#     @classmethod
#     def setUpClass(cls):
#         """Set up class method to mock requests.get with fixtures"""
#         def get_json_side_effect(url):
#             """Side effect function to return appropriate fixture based on URL"""
#             if url == "https://api.github.com/orgs/test_org":
#                 return cls.org_payload
#             elif url == cls.org_payload.get("repos_url"):
#                 return cls.repos_payload
#             return None

#         cls.get_patcher = patch('client.get_json')  # Patch get_json directly
#         cls.mock_get = cls.get_patcher.start()
#         cls.mock_get.side_effect = get_json_side_effect

#     @classmethod
#     def tearDownClass(cls):
#         """Tear down class method to stop the patcher"""
#         cls.get_patcher.stop()

#     def test_public_repos(self):
#         """Test GithubOrgClient.public_repos without license filter"""
#         client = GithubOrgClient("test_org")
#         result = client.public_repos()
#         self.assertEqual(result, self.expected_repos)

#     def test_public_repos_with_license(self):
#         """Test GithubOrgClient.public_repos with license filter"""
#         client = GithubOrgClient("test_org")
#         result = client.public_repos(license="apache-2.0")
#         self.assertEqual(result, self.apache2_repos)

# if __name__ == '__main__':
#     unittest.main()

#!/usr/bin/env python3
"""Unit tests for GithubOrgClient class"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
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

    def test_public_repos_url(self) -> None:
        """Test that GithubOrgClient._public_repos_url returns the correct value"""
        org_name = "test_org"
        expected_repos_url = "https://api.github.com/orgs/test_org/repos"
        mocked_payload = {"repos_url": expected_repos_url}
        
        with patch('client.GithubOrgClient.org',
                  new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mocked_payload
            client = GithubOrgClient(org_name)
            result = client._public_repos_url
            
            self.assertEqual(result, expected_repos_url)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock) -> None:
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
                  new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_repos_url
            client = GithubOrgClient(org_name)
            result = client.public_repos()
            
            self.assertEqual(result, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """Test that GithubOrgClient.has_license returns the correct value"""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


# @parameterized_class([
#     {
#         'org_payload': TEST_PAYLOAD[0][0],
#         'repos_payload': TEST_PAYLOAD[0][1],
#         'expected_repos': TEST_PAYLOAD[0][2],
#         'apache2_repos': TEST_PAYLOAD[0][3]
#     }
# ])
# class TestIntegrationGithubOrgClient(unittest.TestCase):
#     """Integration test case for GithubOrgClient class"""

#     @classmethod
#     def setUpClass(cls) -> None:
#         """Set up class method to mock requests.get with fixtures"""
#         def get_json_side_effect(url: str):
#             """Side effect function to return appropriate fixture based on URL"""
#             if url == "https://api.github.com/orgs/test_org":
#                 return cls.org_payload
#             elif url == cls.org_payload.get("repos_url"):
#                 return cls.repos_payload
#             return None

#         cls.get_patcher = patch('utils.requests.get')
#         cls.mock_get = cls.get_patcher.start()
#         cls.mock_get.return_value.json.side_effect = get_json_side_effect

#     @classmethod
#     def tearDownClass(cls) -> None:
#         """Tear down class method to stop the patcher"""
#         cls.get_patcher.stop()

#     def test_public_repos(self) -> None:
#         """Test GithubOrgClient.public_repos without license filter"""
#         client = GithubOrgClient("test_org")
#         result = client.public_repos()
#         self.assertEqual(result, self.expected_repos)

#     def test_public_repos_with_license(self) -> None:
#         """Test GithubOrgClient.public_repos with license filter"""
#         client = GithubOrgClient("test_org")
#         result = client.public_repos(license="apache-2.0")
#         self.assertEqual(result, self.apache2_repos)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for GithubOrgClient class"""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class method to mock requests.get with fixtures"""
        def get_json_side_effect(url: str):
            """Side effect function to return appropriate fixture based on URL"""
            if url == "https://api.github.com/orgs/test_org":
                return cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                return cls.repos_payload
            return None

        cls.get_patcher = patch('client.get_json')  # Patch client.get_json instead of utils.requests.get
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = get_json_side_effect  # Set side_effect directly on get_json

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test GithubOrgClient.public_repos without license filter"""
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test GithubOrgClient.public_repos with license filter"""
        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)

if __name__ == '__main__':
    unittest.main()