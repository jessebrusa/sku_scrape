from urllib.parse import urlparse


def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


def extract_keywords(item_name):
    keywords = item_name.lower().split()
    try:
        with open('./neglect.txt', 'r') as f:
            neglect_words = set(word.strip() for word in f.read().split())
    except FileNotFoundError:
        neglect_words = set()
    return [word for word in keywords if word not in neglect_words]


def filter_link(url, item_name):
    domain = extract_domain(url)
    keywords = extract_keywords(item_name)
    if domain and keywords:
        for keyword in keywords:
            if keyword not in url.lower():
                return None
        return domain
    return None


def filter_links(links, item_name):
    domain_list = []
    link_dict = {}
    for link in links:
        domain = filter_link(link, item_name)
        if domain and domain not in domain_list:
            domain_list.append(domain)
            link_dict[domain] = link
    return link_dict


if __name__ == "__main__":
    test = {
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
    }

    result = filter_links(test['links'], test['item_name'])
    print(result)