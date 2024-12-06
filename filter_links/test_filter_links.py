import unittest
import json
from filter_links import filter_links

class TestFilterLinks(unittest.TestCase):
    def test_filter_links(self):
        test_cases = [
            {
                "links": [
                    "https://ironcladsentry.com/products/boss-strongbox-7125-7413-top-loader/",
                    "https://ironcladsentry.com/products/another-product/",
                    "https://example.com/products/boss-strongbox-7125-7413-top-loader/",
                    "https://example.com/products/another-product/",
                    "https://anotherdomain.com/products/boss-strongbox-7125-7413-top-loader/",
                    "https://anotherdomain.com/products/another-product/"
                ],
                "item_name": "Boss Strongbox 7125-7413 Top Loader",
                "expected_result": {
                    "ironcladsentry.com": "https://ironcladsentry.com/products/boss-strongbox-7125-7413-top-loader/",
                    "example.com": "https://example.com/products/boss-strongbox-7125-7413-top-loader/",
                    "anotherdomain.com": "https://anotherdomain.com/products/boss-strongbox-7125-7413-top-loader/"
                }
            },
            {
                "links": [
                    "https://example.com/products/another-product/",
                    "https://anotherdomain.com/products/another-product/"
                ],
                "item_name": "Another Product",
                "expected_result": {
                    "example.com": "https://example.com/products/another-product/",
                    "anotherdomain.com": "https://anotherdomain.com/products/another-product/"
                }
            },
            {
                "links": [
                    "https://example.com/products/special-item/",
                    "https://anotherdomain.com/products/special-item/"
                ],
                "item_name": "Special Item",
                "expected_result": {
                    "example.com": "https://example.com/products/special-item/",
                    "anotherdomain.com": "https://anotherdomain.com/products/special-item/"
                }
            },
            # Edge case: No links provided
            {
                "links": [],
                "item_name": "No Links",
                "expected_result": {}
            },
            # Edge case: Links that do not match the item name
            {
                "links": [
                    "https://example.com/products/unrelated-item/",
                    "https://anotherdomain.com/products/unrelated-item/"
                ],
                "item_name": "Nonexistent Item",
                "expected_result": {}
            },
            # Edge case: Links with different domain structures
            {
                "links": [
                    "https://sub.example.com/products/item/",
                    "https://anotherdomain.com/products/item/"
                ],
                "item_name": "Item",
                "expected_result": {
                    "sub.example.com": "https://sub.example.com/products/item/",
                    "anotherdomain.com": "https://anotherdomain.com/products/item/"
                }
            },
            # Edge case: Links with special characters in the item name
            {
                "links": [
                    "https://example.com/products/special-item-123/",
                    "https://anotherdomain.com/products/special-item-123/"
                ],
                "item_name": "Special Item 123",
                "expected_result": {
                    "example.com": "https://example.com/products/special-item-123/",
                    "anotherdomain.com": "https://anotherdomain.com/products/special-item-123/"
                }
            },
            # Edge case: Links with subdomains
            {
                "links": [
                    "https://sub.example.com/products/sub-item/",
                    "https://anotherdomain.com/products/sub-item/"
                ],
                "item_name": "Sub Item",
                "expected_result": {
                    "sub.example.com": "https://sub.example.com/products/sub-item/",
                    "anotherdomain.com": "https://anotherdomain.com/products/sub-item/"
                }
            }
        ]

        results = []
        for case in test_cases:
            result = filter_links(case['links'], case['item_name'])
            passed = result == case['expected_result']
            results.append({
                "item_name": case['item_name'],
                "expected_result": case['expected_result'],
                "actual_result": result,
                "passed": passed
            })

        with open('test_results.json', 'w') as f:
            json.dump(results, f, indent=4)

if __name__ == '__main__':
    unittest.main()