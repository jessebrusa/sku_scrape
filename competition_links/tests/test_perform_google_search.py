import unittest
from unittest.mock import patch
import sys
import os

# Add the project root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from competition_links.collect_links import perform_google_search

class TestPerformGoogleSearch(unittest.TestCase):

    @patch('competition_links.collect_links.search')
    def test_perform_google_search(self, mock_search):
        # Mock the search function to return a fixed set of URLs
        mock_urls = [
            'https://www.example.com',
            'https://www.example.org',
            'https://www.example.net'
        ]
        mock_search.return_value = mock_urls

        # Test with default num_results
        query = "example query"
        result = perform_google_search(query)
        self.assertEqual(len(result), len(mock_urls))
        self.assertEqual(result, mock_urls)

        # Test with a different num_results
        num_results = 2
        mock_search.return_value = mock_urls[:num_results]  # Adjust mock return value
        result = perform_google_search(query, num_results=num_results)
        self.assertEqual(len(result), num_results)
        self.assertEqual(result, mock_urls[:num_results])

    @patch('competition_links.collect_links.search')
    def test_perform_google_search_no_results(self, mock_search):
        # Mock the search function to return no URLs
        mock_search.return_value = []

        query = "no results query"
        result = perform_google_search(query)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()