import requests
import os

def perform_google_search(query, num_results=10, start=1):
    search_url = "https://www.googleapis.com/customsearch/v1"
    api_key = os.getenv('GOOGLE_API_KEY')
    cx = os.getenv('GOOGLE_API_CX')
    
    if not api_key or not cx:
        print("API key or Custom Search Engine ID (cx) is missing.")
        return []

    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'num': num_results,
        'start': start
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def collect_links(item_name, total_results=50):
    url_list = []
    query = f'shop {item_name}'
    num_results_per_page = 10
    start = 1

    while len(url_list) < total_results:
        data = perform_google_search(query, num_results=num_results_per_page, start=start)
        if not data or 'items' not in data:
            break
        urls = [item['link'] for item in data['items']]
        url_list.extend(urls)
        start += num_results_per_page

        # Check if there are more results available
        if 'queries' in data and 'nextPage' not in data['queries']:
            print("No more pages available.")
            break

        print(f"Retrieved {len(url_list)} links so far...")

    return url_list[:total_results]

if __name__ == "__main__":
    item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
    links = collect_links(item_name, total_results=50)
    print(links)
    print(f"Total links retrieved: {len(links)}")