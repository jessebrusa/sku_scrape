from playwright.sync_api import sync_playwright


def download_html_with_playwright(url):
    def fetch_html(url, headless):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page()
            page.goto(url)
            page_content = page.content()
            browser.close()
            return page_content

    try:
        # Attempt to fetch HTML in headless mode
        page_content = fetch_html(url, headless=True)
    except Exception as e:
        print(f"Headless mode failed: {e}")
        print("Reattempting in non-headless mode...")
        try:
            # Attempt to fetch HTML in non-headless mode
            page_content = fetch_html(url, headless=False)
        except Exception as e:
            print(f"Non-headless mode failed: {e}")
            return None

    # Save the HTML content to ./temp.html
    try:
        with open('./temp.html', 'w', encoding='utf-8') as file:
            file.write(page_content)
        print(f"HTML content with JavaScript successfully saved to ./temp.html")
    except Exception as e:
        print(f"Failed to save HTML content: {e}")
        return None

    return None

if __name__ == "__main__":
    url = 'https://www.ralphs.com/p/barska-security-safe-black-1-20-cu-ft-cap-ax13090/0079027200375'
    
    # Use Playwright to download HTML with JavaScript loaded
    download_html_with_playwright(url)