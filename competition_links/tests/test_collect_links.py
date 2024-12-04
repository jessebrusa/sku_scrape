import unittest
from unittest.mock import patch
import sys
import os

# Add the project root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from competition_links.collect_links import collect_links

class TestCollectLinks(unittest.TestCase):

    @patch('competition_links.collect_links.perform_google_search')
    def test_collect_links(self, mock_perform_google_search):
        # Mock the perform_google_search function to return a fixed set of URLs
        mock_urls = [
            'https://www.example.com',
            'https://www.example.org',
            'https://www.example.net'
        ]
        mock_perform_google_search.return_value = mock_urls

        # Test with a single SKU
        sku_list = ['12345']
        result = collect_links(sku_list)
        self.assertEqual(result, mock_urls)

        # Test with multiple SKUs
        sku_list = ['12345', '67890']
        result = collect_links(sku_list)
        self.assertEqual(result, mock_urls)  # Only the first SKU's URLs are returned

    @patch('competition_links.collect_links.perform_google_search')
    def test_collect_links_no_results(self, mock_perform_google_search):
        # Mock the perform_google_search function to return no URLs
        mock_perform_google_search.return_value = []

        sku_list = ['12345']
        result = collect_links(sku_list)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()