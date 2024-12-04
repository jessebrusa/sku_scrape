from playwright.sync_api import sync_playwright

def fetch_data(url, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)
        
        data_element = page.query_selector('#content > div:nth-child(1) > div.ProductDetails--Content-Wrapper > div.ProductDetails--Content.mt-16 > div.ProductDetails--RightColumn.px-8 > div > div:nth-child(5) > div > div.flex.flex-row.w-full > div.flex.flex-col.w-1\\/2.items-start.p-8 > div > data')
        if data_element:
            data_value = data_element.get_attribute('value')
            browser.close()
            return data_value
        else:
            browser.close()
            return None

def main():
    url = 'https://www.kingsoopers.com/p/barska-security-safe-black-1-20-cu-ft-cap-ax13090/0079027200375'  # Replace with your desired URL
    try:
        data_value = fetch_data(url, headless=True)
        if data_value is None:
            raise Exception("Data element not found in headless mode")
        print(f"Data value (headless): {data_value}")
    except Exception as e:
        print(f"Headless mode failed: {e}")
        print("Reattempting in non-headless mode...")
        try:
            data_value = fetch_data(url, headless=False)
            if data_value is None:
                raise Exception("Data element not found in non-headless mode")
            print(f"Data value (non-headless): {data_value}")
        except Exception as e:
            print(f"Non-headless mode failed: {e}")

if __name__ == "__main__":
    main()