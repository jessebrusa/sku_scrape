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
            if keyword in url.lower():
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
    link = 'https://www.amazon.com/Armasight-Collector-Thermal-Riflescope-1-5-6x19mm/dp/B0D2WQM4BR'
    item_name = 'Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight'
    result = filter_links([link], item_name)
    print(result)