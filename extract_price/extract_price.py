from bs4 import BeautifulSoup
import re
import os
from fuzzywuzzy import fuzz
import statistics

delete_html_files = False

def prioritize_price_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_elements = []

    # Extract relevant tags
    for tag in soup.find_all(['p', 'div', 'span', 'strong', 's', 'small', 'mark', 'data']):
        text = tag.get_text()
        # Filter by money symbols and exclude certain keywords and phone numbers
        if re.search(r'[\$\€\£]', text) and not re.search(r'(shipping|order|total|save|discount|off|tel:|list price|page|win)', text, re.IGNORECASE):
            # Exclude elements with specific classes or IDs
            if not tag.find_parent(class_='save-amount-wrap'):
                # Exclude elements with "List" or "list" in the same span or right before
                if not (tag.find_previous_sibling(text=re.compile(r'list', re.IGNORECASE)) or re.search(r'list', text, re.IGNORECASE)):
                    price_elements.append(tag)

    return price_elements

def prioritize_prices(price_elements):
    prioritized_prices = []

    for element in price_elements:
        text = element.get_text()
        # Check for contextual clues
        if re.search(r'(current|sale|discount|now)\s*price', text, re.IGNORECASE):
            prioritized_prices.append(element)
        # Prioritize elements with specific classes or IDs
        elif 'price__current' in element.get('class', []):
            prioritized_prices.append(element)
        # Prioritize elements wrapped in <ins> tags
        elif element.find('ins'):
            prioritized_prices.append(element.find('ins'))
        # Prioritize elements with data-price or data-value attribute
        elif element.has_attr('data-price') or element.has_attr('data-value'):
            prioritized_prices.append(element)
        # Prioritize elements with data-price-amount attribute and data-price-type="finalPrice"
        elif element.has_attr('data-price-amount') and element.get('data-price-type') == 'finalPrice':
            prioritized_prices.append(element)
        # Prioritize elements with complex price structures
        elif element.find('sup') and element.find('span'):
            prioritized_prices.append(element)
        # Prioritize elements with aria-label attribute containing price
        elif element.has_attr('aria-label') and re.search(r'[\$\€\£]', element['aria-label']):
            prioritized_prices.append(element)

    # If no prioritized prices found, return all price elements
    if not prioritized_prices:
        return price_elements

    return prioritized_prices

def clean_price(price_text):
    # Remove any non-numeric characters except the decimal point
    price_cleaned = re.sub(r'[^\d.]', '', price_text)
    try:
        return round(float(price_cleaned), 2)
    except ValueError:
        return None

def get_current_price(html_content, item_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Check if there are multiple product listings on the page
    product_listings = soup.find_all('li', class_='product')
    if len(product_listings) > 1:
        for product in product_listings:
            product_name_element = product.find('h4', class_='card-title')
            if product_name_element and fuzz.partial_ratio(item_name.lower(), product_name_element.get_text().lower()) > 80:
                price_element = product.find('div', class_='card-text')
                if price_element:
                    price = find_price_in_element(price_element)
                    if price:
                        return clean_price(price)
    
    # If no multiple product listings or no match found, use the original method
    price_elements = prioritize_price_tags(html_content)
    prioritized_prices = prioritize_prices(price_elements)

    for element in prioritized_prices:
        if element.find('sup') and element.find('span'):
            price_text = ''.join([e.get_text() for e in element.find_all(['sup', 'span'])])
        else:
            price_text = element.get_text().strip()
        
        if "List" in price_text:
            continue
        
        price = clean_price(price_text)
        if price is not None and 1000 <= price <= 10000:  # Ensure the price is within a reasonable range
            return price

    return None

def find_price_in_element(element):
    price_patterns = [r'\$\d+(\.\d{2})?', r'\d+(\.\d{2})?\s?USD', r'\d{1,3}(,\d{3})*(\.\d{2})?']
    
    for pattern in price_patterns:
        match = re.search(pattern, element.get_text())
        if match:
            return match.group().strip()
    
    return None

def extract_price_list(price_dict, item_name):
    keys_to_remove = []
    for key, value in price_dict.items():
        if 'file_path' in value:
            html_file = value['file_path']
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            price = get_current_price(html_content, item_name)
            if price is not None:
                price_dict[key]['value'] = price
            else:
                keys_to_remove.append(key)

            # if delete_html_files:
            #     os.remove(html_file)
        else:
            print(f"No file_path for key {key}, URL: {value['url']}")
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del price_dict[key]
    
    return price_dict

def filter_outliers(price_dict):
    prices = [float(value['value']) for value in price_dict.values()]
    if not prices:
        return price_dict

    mean = statistics.mean(prices)
    try:
        std_dev = statistics.stdev(prices)
        filtered_prices = [price for price in prices if abs(price - mean) <= 2 * std_dev]
    except statistics.StatisticsError:
        # If there are not enough data points to calculate stdev, return the original prices
        filtered_prices = prices

    filtered_price_dict = {key: value for key, value in price_dict.items() if float(value['value']) in filtered_prices}

    return filtered_price_dict

if __name__ == "__main__":
    price_dict = {
        0: {'url': 'https://www.holdupdisplays.com/black-camo-gun-wall-bundle-hd100-bc/?srsltid=AfmBOorvSo1leB3tV49qa0qlBCT3-L8KjUjrUcfpQ9sEPTgL6W9khHQ-'},
        1: {'url': 'https://www.safeandvaultstore.com/products/hold-up-displays-black-camo-gun-wall-bundle-hd100-bc?srsltid=AfmBOoqwormUU6-BL2R5LidreCZ7VnM_X-nCrHfdnMEUupfXKjZOjkLc', 'file_path': 'temp/1.html'},
        2: {'url': 'https://homesafesusa.com/products/hold-up-gun-wall-display-black-camo-hd100-bc?srsltid=AfmBOoqcHsLeKxdBKkLXK2Hw4vdswhSV7BbnHrvZWzmgqiPkV7OT1491', 'file_path': 'temp/2.html'},
        3: {'url': 'https://ironcladsentry.com/products/hold-up-displays-hd100-bc-black-camo-gun-wall-bundle', 'file_path': 'temp/3.html'},
        4: {'url': 'https://www.smartlockbox.shop/product/category-gun-wall-armory-kits-brand-hold-up-displays-hold-up-displays-black-camo-gun-wall-bundle-hd100-bc/', 'file_path': 'temp/4.html'}
    }
    item_name = "Collector 320 1.5-6x19 Compact Thermal Weapon Sight"
    updated_price_dict = extract_price_list(price_dict, item_name)
    filtered_price_dict = filter_outliers(updated_price_dict)
    print(f"Filtered price_dict: {filtered_price_dict}")