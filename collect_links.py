from googlesearch import search
from urllib.parse import urlparse

def perform_google_search(query, num_results=12):
    urls = []
    for url in search(query, num_results=num_results):
        urls.append(url)
    return urls

def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def write_url_list(url_list, filename):
    processed_domains = set()
    
    # Read existing domains from the output file
    try:
        with open(filename, 'r') as f:
            for line in f:
                domain = get_domain(line.strip())
                processed_domains.add(domain)
    except FileNotFoundError:
        pass  # If the file doesn't exist, continue without error
    
    with open(filename, 'a') as f:
        for url in url_list:
            domain = get_domain(url)
            if domain not in processed_domains:
                f.write(url + '\n')
                processed_domains.add(domain)

def write_domain_list(url_list, filename):
    processed_domains = set()
    
    # Read existing domains from the output file
    try:
        with open(filename, 'r') as f:
            for line in f:
                processed_domains.add(line.strip())
    except FileNotFoundError:
        pass  # If the file doesn't exist, continue without error
    
    with open(filename, 'a') as f:
        for url in url_list:
            domain = get_domain(url)
            if domain not in processed_domains:
                f.write(domain + '\n')
                processed_domains.add(domain)

def main():
    sku_list = ['HD100-BC', 'MIRA403 BODY ARMOR PLATE LEVEL 4 NIJ', 'BC-TS-33901', 'NRA-EIC COMBAT',
                'AX13090', '335-01', 'NSGNYX15M5G9DX2', 'TAVT36WN9COLL102', 'TAVT36MNASIDE101',
                'TIBNBX4381L', '403018', 'B1755111']
    for sku in sku_list:
        query = f'SKU {sku}'
        url_list = perform_google_search(query)
        # write_url_list(url_list, f'{sku}_urls.txt')
        write_domain_list(url_list, 'domains.txt')

if __name__ == "__main__":
    main()