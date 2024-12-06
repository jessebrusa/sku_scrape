from googlesearch import search


default_num_results = 50


def perform_google_search(query, num_results=default_num_results):
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    return urls


def collect_links(upc):
    url_list = []
    urls = perform_google_search(f'UPC: {upc}')
    url_list.extend(urls)
        
    return url_list


if __name__ == "__main__":
    collect_links()