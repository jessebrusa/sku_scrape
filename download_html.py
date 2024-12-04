import requests
from playwright.sync_api import sync_playwright

def download_html(url, file_destination):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(file_destination, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML content successfully saved to {file_destination}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        

def download_html_with_playwright(url, file_destination):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page_content = page.content()
            with open(file_destination, 'w', encoding='utf-8') as file:
                file.write(page_content)
            print(f"HTML content with JavaScript successfully saved to {file_destination}")
            browser.close()
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto(url)
                page_content = page.content()
                try:
                    data_element = page.query_selector('#content > div:nth-child(1) > div.ProductDetails--Content-Wrapper > div.ProductDetails--Content.mt-16 > div.ProductDetails--RightColumn.px-8 > div > div:nth-child(5) > div > div.flex.flex-row.w-full > div.flex.flex-col.w-1\\/2.items-start.p-8 > div > data')
                    if data_element:
                        data_value = data_element.get_attribute('value')
                        browser.close()
                        return float(data_value)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    browser.close()
                    return None
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = 'https://www.homedepot.com/p/BARSKA-Digital-Keypad-Security-Safe-1-2-cu-ft-AX13090/321074933'
    destination = './barska_safe.html'
    
    # # Use requests to download HTML
    # download_html(url, destination)
    
    # Use Playwright to download HTML with JavaScript loaded
    destination_with_js = './barska_safe_with_js.html'
    download_html_with_playwright(url, destination_with_js)