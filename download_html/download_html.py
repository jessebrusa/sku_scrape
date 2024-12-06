from playwright.sync_api import sync_playwright

def download_html_playwright_non_headless(url, page):
    try:
        page.goto(url, wait_until='load')
        page_content = page.content()
        return page_content
    except Exception as e:
        print(f"An error occurred with Playwright (non-headless): {e}")
        return None

def download_html(url, page):
    print(f"Attempting to download HTML for {url} using Playwright (non-headless)...")
    html = download_html_playwright_non_headless(url, page)
    if html:
        return html

    print(f"Failed to download HTML for {url} using all methods.")
    return None

def save_html(price_dict):
    url_list_valid = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        for key, value in price_dict.items():
            url = value['url']
            html = download_html(url, page)
            if html:
                filename = f'temp/{key}.html'
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(html)
                url_list_valid.append(url)
                price_dict[key]['file_path'] = filename
            else:
                print(f'No html downloaded for {url}')
        browser.close()
    return price_dict

if __name__ == "__main__":
    price_dict = {
        0: {'url': 'https://www.ralphs.com/p/barska-security-safe-black-1-20-cu-ft-cap-ax13090/0079027200375'},
        1: {'url': 'https://www.holdupdisplays.com/black-camo-gun-wall-bundle-hd100-bc/?srsltid=AfmBOopwMv_AwCob1mDoBu1ZddQnknCC9ZmcMLFFWpvRx_gsgHfQDVwu'}
    }
    valid_links = save_html(price_dict)
    print(f"Valid links: {valid_links}")