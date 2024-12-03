import requests
from bs4 import BeautifulSoup
import re
import os
import json
from download_html import download_html_with_playwright

def extract_prices(html):
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

def get_current_price(source):
    if os.path.isfile(source):
        # Read HTML content from file
        with open(source, 'r', encoding='utf-8') as file:
            html_content = file.read()
    else:
        # Fetch HTML content from URL
        try:
            response = requests.get(source, timeout=10)
            response.raise_for_status()
            html_content = response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {source}: {e}")
            return None

    price_elements = extract_prices(html_content)
    prioritized_prices = prioritize_prices(price_elements)

    for element in prioritized_prices:
        # Handle complex price structures
        if element.find('sup') and element.find('span'):
            price_text = ''.join([e.get_text() for e in element.find_all(['sup', 'span'])])
        else:
            price_text = element.get_text().strip()
        
        # Exclude elements with "List" in the text
        if "List" in price_text:
            continue
        
        price = clean_price(price_text)
        if price is not None:
            return price

    return None

if __name__ == "__main__":
    total_count = 0
    pass_count = 0


    with open('results.txt', 'w') as file:
        file.write('')  # Clear the file at the start

    with open('safe.json', 'r') as json_file:
        data = json.load(json_file) 

    for key, value in data.items():
        url = key
        correct_price = value

        current_price = get_current_price(url)

        if current_price is None:
            print(f'Fetching {url} with Playwright...')
            download_html_with_playwright(url, 'barska_safe_with_js.html')
            current_price = get_current_price('barska_safe_with_js.html')
            if current_price is None:
                print(f'Failed to fetch {url}')
                result = f'fail\nError fetching {url}'
                continue

        if round(current_price, 2) == round(correct_price, 2):
            print(f'PASS: {url}')
            result = 'pass'
            pass_count += 1
        else:
            print(f'FAIL: {url}')
            result = f'fail\nExpected: {correct_price}\nActual: {current_price}\nURL: {url}'

        
        with open('results.txt', 'a') as file:
            file.write(f'{result}\n\n')

        total_count += 1

    fail_count = total_count - pass_count
    # Print and write out the pass and fail numbers
    summary = f'Pass: {pass_count}\nFail: {fail_count}\n'
    print(summary)
    with open('results.txt', 'a') as file:
        file.write(summary)