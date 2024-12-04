from googlesearch import search


def perform_google_search(query, num_results=35):
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    return urls


def collect_links(sku_list):
    for sku in sku_list:
        query = f'SKU {sku}'
        url_list = perform_google_search(query)
        
        return url_list


if __name__ == "__main__":
    collect_links()