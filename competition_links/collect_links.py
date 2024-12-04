from googlesearch import search


default_num_results = 10


def perform_google_search(query, num_results=default_num_results):
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    return urls


def collect_links(sku):
    if not isinstance(sku, list):
        sku = [sku]
        
    url_list = []
    for item in sku:
        query = f'SKU {item}'
        urls = perform_google_search(query)
        url_list.extend(urls)
        
    return url_list


if __name__ == "__main__":
    collect_links()