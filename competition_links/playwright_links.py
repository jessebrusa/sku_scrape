from playwright.sync_api import sync_playwright

def collect_google_links(item_name, num_links, keywords):
    links = set()  # Use a set to store unique links
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        query = f'shop {item_name}'
        page.goto(f'https://www.google.com/search?q={query}')

        while len(links) < num_links:
            # Extract links from the search results
            search_results = page.query_selector_all('a')
            for result in search_results:
                href = result.get_attribute('href')
                if href and href.startswith('https') and "google" not in href.lower():
                    # Filter out links that are just domains or end with .com/
                    if len(href.split('/')) > 3 and not href.endswith('.com/'):
                        # Check if the link contains any of the keywords
                        if any(keyword.lower() in href.lower() for keyword in keywords):
                            links.add(href)  # Add link to the set to ensure uniqueness

            # Go to the next page if more links are needed
            if len(links) < num_links:
                next_button = page.query_selector('a#pnnext')
                if next_button:
                    next_button.click()
                    page.wait_for_load_state('networkidle')
                else:
                    print("No more pages available.")
                    break

        browser.close()
    
    return list(links)  # Convert the set to a list

if __name__ == '__main__':
    # Example usage
    query = "Armasight Collector 320 1.5-6x19 Compact Thermal Weapon Sight"
    num_links = 200
    keywords = ['armasight', 'collector', '320', '1.5-6x19', 'compact', 'thermal', 'weapon', 'sight']
    links = collect_google_links(query, num_links, keywords)

    # Write the links to a text file
    with open('playwright.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')

    print(f"Total links retrieved: {len(links)}")