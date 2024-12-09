import os
import re
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

def extract_price_from_html(file_path, item_name):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    # Check for meta tag with price
    meta_price = soup.find('meta', {'property': 'product:price:amount'})
    if meta_price and meta_price.get('content'):
        return meta_price['content']
    
    # Find the element with the closest match to the item name
    elements = soup.find_all(text=True)
    best_match = None
    highest_ratio = 0
    
    for element in elements:
        ratio = fuzz.partial_ratio(item_name.lower(), element.lower())
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = element
    
    if not best_match:
        return None
    
    # Traverse up the DOM tree to find the price
    current_element = best_match.parent
    while current_element:
        price = find_price_in_element(current_element)
        if price:
            return price
        current_element = current_element.parent
    
    return None

def find_price_in_element(element):
    price_patterns = [r'\$\d+(\.\d{2})?', r'\d+(\.\d{2})?\s?USD', r'\d{1,3}(,\d{3})*(\.\d{2})?']
    
    for pattern in price_patterns:
        match = re.search(pattern, element.get_text())
        if match:
            return match.group().strip()
    
    return None

def extract_prices_from_dict(data_dict, item_name):
    prices = {}
    for key, details in data_dict.items():
        file_path = details['file_path']
        try:
            price = extract_price_from_html(file_path, item_name)
            if price:
                prices[key] = price
        except FileNotFoundError as e:
            print(e)
    return prices