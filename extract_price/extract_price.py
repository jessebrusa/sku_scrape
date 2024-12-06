from bs4 import BeautifulSoup
import re
import os

delete_html_files = False

def prioritize_price_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_elements = []

    # Extract relevant tags
    for tag in soup.find_all(['p', 'div', 'span', 'strong', 's', 'small', 'mark', 'data']):
        text = tag.get_text()
        # Filter by money symbols and exclude certain keywords and phone numbers
        if re.search(r'[\$\€\£]', text) and not re.search(r'(shipping|order|total|save|discount|off|tel:|list price)', text, re.IGNORECASE):
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

def get_current_price(html_content):
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
        if price is not None:
            return price

    return None

def extract_price_list(price_dict):
    keys_to_remove = []
    for key, value in price_dict.items():
        if 'file_path' in value:
            html_file = value['file_path']
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            price = get_current_price(html_content)
            if price is not None:
                price = round(float(price), 2)
                if price != 0:
                    price_dict[key]['value'] = price
            else:
                keys_to_remove.append(key)

            if delete_html_files:
                os.remove(html_file)
        else:
            print(f"No file_path for key {key}, URL: {value['url']}")
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del price_dict[key]
    
    return price_dict

if __name__ == "__main__":
    price_dict = {
        0: {'url': 'https://www.holdupdisplays.com/black-camo-gun-wall-bundle-hd100-bc/?srsltid=AfmBOorvSo1leB3tV49qa0qlBCT3-L8KjUjrUcfpQ9sEPTgL6W9khHQ-'},
        1: {'url': 'https://www.safeandvaultstore.com/products/hold-up-displays-black-camo-gun-wall-bundle-hd100-bc?srsltid=AfmBOoqwormUU6-BL2R5LidreCZ7VnM_X-nCrHfdnMEUupfXKjZOjkLc', 'file_path': 'temp/1.html'},
        2: {'url': 'https://homesafesusa.com/products/hold-up-gun-wall-display-black-camo-hd100-bc?srsltid=AfmBOoqcHsLeKxdBKkLXK2Hw4vdswhSV7BbnHrvZWzmgqiPkV7OT1491', 'file_path': 'temp/2.html'},
        3: {'url': 'https://ironcladsentry.com/products/hold-up-displays-hd100-bc-black-camo-gun-wall-bundle', 'file_path': 'temp/3.html'},
        4: {'url': 'https://www.smartlockbox.shop/product/category-gun-wall-armory-kits-brand-hold-up-displays-hold-up-displays-black-camo-gun-wall-bundle-hd100-bc/', 'file_path': 'temp/4.html'}
    }
    updated_price_dict = extract_price_list(price_dict)
    print(f"Updated price_dict: {updated_price_dict}")