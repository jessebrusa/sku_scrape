import requests
from playwright.sync_api import sync_playwright

def download_html_requests(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status() 
        return response.text
    except requests.exceptions.RequestException as e:
        return None

def download_html_playwright(url, headless=True):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(url, wait_until='load')
            page_content = page.content()
            browser.close()
            return page_content
    except Exception as e:
        return None

def download_html(url):
    html = download_html_requests(url)
    if html:
        return html

    html = download_html_playwright(url, headless=True)
    if html:
        return html
    
    html = download_html_playwright(url, headless=False)
    if html:
        return html

    return None

def save_html(price_dict):
    url_list_valid = []
    for key, value in price_dict.items():
        url = value['url']
        html = download_html(url)
        if html:
            filename = f'temp/{key}.html'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(html)
            url_list_valid.append(url)
            price_dict[key]['file_path'] = filename

    return price_dict

if __name__ == "__main__":
    price_dict = {
        0: {'url': 'https://www.ralphs.com/p/barska-security-safe-black-1-20-cu-ft-cap-ax13090/0079027200375'},
        1: {'url': 'https://www.holdupdisplays.com/black-camo-gun-wall-bundle-hd100-bc/?srsltid=AfmBOopwMv_AwCob1mDoBu1ZddQnknCC9ZmcMLFFWpvRx_gsgHfQDVwu'}
    }
    valid_links = save_html(price_dict)
    print(f"Valid links: {valid_links}")