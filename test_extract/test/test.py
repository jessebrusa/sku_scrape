import json
import os
import sys

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extract_links import filter_links

def run_tests(test_file, output_file):
    with open(test_file, 'r') as file:
        test_data = json.load(file)

    results = []
    for test in test_data['tests']:
        links = test['links']
        item_name = test['item_name']
        expected_result = test['expected_result']

        result = filter_links(links, item_name)
        test_result = {
            'item_name': item_name,
            'expected_result': expected_result,
            'actual_result': result,
            'passed': result == expected_result
        }
        results.append(test_result)

    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)

if __name__ == "__main__":
    run_tests('test_data.json', 'test_results.json')