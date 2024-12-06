from googlesearch import search

default_num_results = 150

def perform_google_search(query, num_results=default_num_results):
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    return urls

def collect_links(item_name):
    url_list = []
    query = f'shop {item_name}'
    urls = perform_google_search(query, num_results=default_num_results)
    url_list.extend(urls)
        
    return url_list

if __name__ == "__main__":
    item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
    links = collect_links(item_name)
    print(links)